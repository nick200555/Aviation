# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt
#
# AeroSpaceOS — Spaceflight API
# Provides whitelisted REST endpoints for telemetry ingestion, trajectory
# computation, ground-pass scheduling, conjunction probability, and propellant.

import frappe
import math
from frappe.utils import now_datetime, cint, flt


# ─────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────
EARTH_RADIUS_KM = 6371.0
GM = 398600.4418          # km³/s²   Earth standard gravitational parameter
PROPELLANT_LOW_PCT = 15   # % threshold for low-propellant warning


# ─────────────────────────────────────────────────────────────
# 1. ingest_telemetry
# ─────────────────────────────────────────────────────────────
@frappe.whitelist()
def ingest_telemetry(spacecraft, telemetry_data):
    """
    Ingests spacecraft telemetry from Mission Control / ground station downlink.

    Updates: propellant level, battery voltage, solar array power, last_telemetry_utc.

    :param spacecraft: Name of the Spacecraft Asset document (e.g. SAT-LEO-109)
    :param telemetry_data: dict | JSON string with keys:
        propellant_kg, battery_voltage, solar_power
    :returns: dict with status, spacecraft, and updated fields
    """
    if isinstance(telemetry_data, str):
        import json
        telemetry_data = json.loads(telemetry_data)

    if not frappe.db.exists("Spacecraft Asset", spacecraft):
        frappe.throw(f"Spacecraft Asset '{spacecraft}' not found.", frappe.DoesNotExistError)

    doc = frappe.get_doc("Spacecraft Asset", spacecraft)

    # Apply telemetry fields
    propellant_kg = flt(telemetry_data.get("propellant_kg", doc.current_propellant_level_kg))
    battery_v     = flt(telemetry_data.get("battery_voltage", doc.battery_voltage_v or 0))
    solar_w       = flt(telemetry_data.get("solar_power", doc.solar_array_power_w or 0))

    doc.current_propellant_level_kg = propellant_kg
    doc.battery_voltage_v           = battery_v
    doc.solar_array_power_w         = solar_w
    doc.last_telemetry_utc          = now_datetime()

    doc.save(ignore_permissions=True)

    # Fire low-propellant alert if below threshold
    if doc.propellant_capacity_kg and doc.propellant_capacity_kg > 0:
        pct = (propellant_kg / doc.propellant_capacity_kg) * 100
        if pct < PROPELLANT_LOW_PCT:
            _trigger_low_propellant_notification(doc, pct)

    frappe.db.commit()

    return {
        "status": "success",
        "spacecraft": spacecraft,
        "updated": {
            "propellant_kg": propellant_kg,
            "battery_voltage_v": battery_v,
            "solar_array_power_w": solar_w,
            "last_telemetry_utc": str(doc.last_telemetry_utc)
        }
    }


def _trigger_low_propellant_notification(doc, pct):
    """Internal helper: create a Notification Log for low propellant."""
    try:
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"🛸 LOW PROPELLANT: {doc.spacecraft_name} at {round(pct, 1)}%",
            "email_content": (
                f"Spacecraft {doc.spacecraft_name} ({doc.name}) propellant is at "
                f"{round(pct, 1)}% ({doc.current_propellant_level_kg} kg remaining of "
                f"{doc.propellant_capacity_kg} kg capacity). Immediate ground review required."
            ),
            "for_user": "Administrator",
            "type": "Alert"
        }).insert(ignore_permissions=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Low Propellant Notification Failed")


# ─────────────────────────────────────────────────────────────
# 2. get_satellite_trajectory
# ─────────────────────────────────────────────────────────────
@frappe.whitelist()
def get_satellite_trajectory(spacecraft):
    """
    Returns the latest Orbit Parameter record for a spacecraft and
    computes the ground-track velocity and estimated position zone.

    :param spacecraft: Name of the Spacecraft Asset document
    :returns: dict with orbital elements, computed speed, and ground track estimate
    """
    if not frappe.db.exists("Spacecraft Asset", spacecraft):
        frappe.throw(f"Spacecraft Asset '{spacecraft}' not found.", frappe.DoesNotExistError)

    orbit = frappe.db.get_value(
        "Orbit Parameter",
        {"spacecraft": spacecraft},
        [
            "name", "epoch_utc", "semi_major_axis_km", "eccentricity",
            "inclination_deg", "apogee_km", "perigee_km",
            "orbital_period_minutes", "mean_motion_rev_per_day"
        ],
        as_dict=True,
        order_by="epoch_utc desc"
    )

    if not orbit:
        frappe.throw(
            f"No Orbit Parameter records found for spacecraft '{spacecraft}'.",
            frappe.DoesNotExistError
        )

    # Compute orbital speed at perigee (vis-viva equation approximation)
    a = flt(orbit.get("semi_major_axis_km"))
    e = flt(orbit.get("eccentricity"))
    r_perigee = a * (1 - e)  # km from Earth center

    if a > 0 and r_perigee > 0:
        # Vis-Viva: v = sqrt(GM * (2/r - 1/a))
        v_perigee_kms = math.sqrt(GM * (2 / r_perigee - 1 / a))
    else:
        v_perigee_kms = 0

    return {
        "spacecraft": spacecraft,
        "latest_epoch": str(orbit.get("epoch_utc")),
        "orbit_parameter_name": orbit.get("name"),
        "semi_major_axis_km": orbit.get("semi_major_axis_km"),
        "eccentricity": orbit.get("eccentricity"),
        "inclination_deg": orbit.get("inclination_deg"),
        "apogee_km": orbit.get("apogee_km"),
        "perigee_km": orbit.get("perigee_km"),
        "orbital_period_minutes": orbit.get("orbital_period_minutes"),
        "mean_motion_rev_per_day": orbit.get("mean_motion_rev_per_day"),
        "computed": {
            "perigee_speed_kms": round(v_perigee_kms, 4),
            "perigee_speed_kmh": round(v_perigee_kms * 3600, 1)
        }
    }


# ─────────────────────────────────────────────────────────────
# 3. get_ground_station_schedule
# ─────────────────────────────────────────────────────────────
@frappe.whitelist()
def get_ground_station_schedule(spacecraft=None, ground_station=None, limit=20):
    """
    Returns scheduled Ground Station Pass records for a spacecraft or station.

    :param spacecraft: Optional filter by Spacecraft Asset name
    :param ground_station: Optional filter by ground station name
    :param limit: Max number of records to return (default 20)
    :returns: list of pass schedule dicts
    """
    filters = {}
    if spacecraft:
        filters["spacecraft"] = spacecraft
    if ground_station:
        filters["ground_station_name"] = ["like", f"%{ground_station}%"]

    passes = frappe.get_all(
        "Ground Station Pass",
        filters=filters,
        fields=[
            "name", "spacecraft", "ground_station_name", "ground_station_location",
            "pass_start_utc", "pass_end_utc", "max_elevation_deg",
            "downlink_frequency_mhz", "telemetry_status", "data_volume_mb"
        ],
        order_by="pass_start_utc asc",
        limit=cint(limit)
    )

    # Compute duration for each pass
    for p in passes:
        if p.get("pass_start_utc") and p.get("pass_end_utc"):
            from frappe.utils import time_diff_in_seconds
            secs = time_diff_in_seconds(p["pass_end_utc"], p["pass_start_utc"])
            p["duration_minutes"] = round(secs / 60, 2)
        else:
            p["duration_minutes"] = 0

    return {"count": len(passes), "passes": passes}


# ─────────────────────────────────────────────────────────────
# 4. calculate_collision_probability
# ─────────────────────────────────────────────────────────────
@frappe.whitelist()
def calculate_collision_probability(spacecraft, debris_catalog_id, miss_distance_meters,
                                    relative_velocity_kms=None, combined_covariance_m=None):
    """
    Estimates collision probability (Pc) using a simplified 2D Foster/Chan model.

    For production, this would interface with NASA CARA or ESA SOCRATES.
    Here we implement a deterministic probability estimate based on
    miss distance, relative velocity, and combined position covariance.

    :param spacecraft: Spacecraft Asset name
    :param debris_catalog_id: NORAD object catalog number
    :param miss_distance_meters: Closest approach miss distance in meters
    :param relative_velocity_kms: Relative velocity at TCA in km/s (optional, default 7.5)
    :param combined_covariance_m: Combined 1-sigma position uncertainty in meters (optional, default 200)
    :returns: dict with Pc estimate and risk classification
    """
    miss_d = flt(miss_distance_meters)
    rel_v  = flt(relative_velocity_kms) if relative_velocity_kms else 7.5   # typical LEO rel velocity
    sigma  = flt(combined_covariance_m) if combined_covariance_m else 200.0  # 200m combined 1-sigma

    # Hard body radius (collision cross-section radius in meters, typical satellite ~5-10m)
    hbr = 10.0

    # Simplified Foster 2D probability calculation
    # Pc ≈ (π * hbr²) / (2π * σ²) * exp(-0.5 * (miss_d/σ)²)
    if sigma <= 0:
        frappe.throw("Combined covariance must be positive.")

    # Combined collision cross-section radius
    r_c = hbr  # meters
    sigma_combined = sigma

    # 2D Gaussian miss distance probability
    if miss_d >= 0:
        exponent = -0.5 * ((miss_d / sigma_combined) ** 2)
        Pc = ((math.pi * r_c ** 2) / (2 * math.pi * sigma_combined ** 2)) * math.exp(exponent)
    else:
        Pc = 0

    # Risk classification
    if Pc >= 1e-4 or miss_d <= 500:
        risk_level = "Critical"
    elif Pc >= 1e-5 or miss_d <= 2000:
        risk_level = "Red"
    elif Pc >= 1e-6:
        risk_level = "Yellow"
    else:
        risk_level = "Green"

    # Auto-create / update conjunction record if above threshold
    action_required = risk_level in ["Red", "Critical"]

    return {
        "spacecraft": spacecraft,
        "debris_catalog_id": debris_catalog_id,
        "miss_distance_meters": miss_d,
        "relative_velocity_kms": rel_v,
        "combined_covariance_m": sigma,
        "collision_probability": Pc,
        "scientific_notation": f"{Pc:.3e}",
        "risk_level": risk_level,
        "action_required": action_required,
        "message": (
            f"Pc = {Pc:.3e} — Risk Level: {risk_level}. "
            + ("⚠️ Maneuver consideration required." if action_required else "✅ Within safe limits.")
        )
    }


# ─────────────────────────────────────────────────────────────
# 5. update_propellant_levels
# ─────────────────────────────────────────────────────────────
@frappe.whitelist()
def update_propellant_levels(spacecraft, new_level_kg, delta_v_used_mps=None):
    """
    Directly updates the propellant level of a spacecraft asset after a
    maneuver or ground refuelling simulation.

    :param spacecraft: Spacecraft Asset name
    :param new_level_kg: New propellant level in kg
    :param delta_v_used_mps: Optional Delta-V expended in m/s (to reduce budget)
    :returns: dict with updated propellant state
    """
    if not frappe.db.exists("Spacecraft Asset", spacecraft):
        frappe.throw(f"Spacecraft Asset '{spacecraft}' not found.", frappe.DoesNotExistError)

    doc = frappe.get_doc("Spacecraft Asset", spacecraft)

    new_level = flt(new_level_kg)
    if new_level < 0:
        frappe.throw("Propellant level cannot be negative.")
    if doc.propellant_capacity_kg and new_level > doc.propellant_capacity_kg:
        frappe.throw(
            f"New propellant level ({new_level} kg) exceeds capacity ({doc.propellant_capacity_kg} kg)."
        )

    old_level = doc.current_propellant_level_kg or 0
    doc.current_propellant_level_kg = new_level

    # Reduce Delta-V budget if maneuver delta-v is provided
    dv_info = {}
    if delta_v_used_mps:
        dv_used = flt(delta_v_used_mps)
        old_dv = doc.delta_v_budget_mps or 0
        doc.delta_v_budget_mps = max(0, old_dv - dv_used)
        dv_info = {"delta_v_used_mps": dv_used, "remaining_delta_v_budget_mps": doc.delta_v_budget_mps}

    doc.last_telemetry_utc = now_datetime()
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "success",
        "spacecraft": spacecraft,
        "previous_level_kg": old_level,
        "new_level_kg": new_level,
        "delta_kg": round(new_level - old_level, 3),
        **dv_info
    }
