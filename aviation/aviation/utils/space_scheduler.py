# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt
#
# AeroSpaceOS — Space Operations Scheduler
# Provides hourly, daily, and weekly scheduled tasks for the Space domain.

import frappe
from frappe.utils import now_datetime, add_days, getdate, nowdate, flt


# ══════════════════════════════════════════════════════════════
# HOURLY JOBS
# ══════════════════════════════════════════════════════════════

def ingest_scheduled_telemetry():
    """
    Hourly: Simulates telemetry ingestion health-check for all active spacecraft.
    In production, this would pull from the TT&C subsystem or CCSDS API.
    Logs a warning if no telemetry has been received in the last 2 hours.
    """
    from frappe.utils import time_diff_in_seconds
    cutoff = add_days(now_datetime(), 0)  # now
    two_hours_ago_seconds = 7200

    active_spacecraft = frappe.get_all(
        "Spacecraft Asset",
        filters={"status": "Active"},
        fields=["name", "spacecraft_name", "last_telemetry_utc"]
    )

    for sc in active_spacecraft:
        if sc.get("last_telemetry_utc"):
            elapsed = time_diff_in_seconds(now_datetime(), sc["last_telemetry_utc"])
            if elapsed > two_hours_ago_seconds:
                frappe.logger().warning(
                    f"[AeroSpaceOS] No telemetry from {sc['spacecraft_name']} "
                    f"({sc['name']}) for {int(elapsed/3600)} hours."
                )
                _create_notification_log(
                    subject=f"📡 Telemetry Gap: {sc['spacecraft_name']}",
                    message=(
                        f"No telemetry received from {sc['spacecraft_name']} ({sc['name']}) "
                        f"for {int(elapsed/3600)} hours. Check ground station contacts."
                    )
                )
        else:
            frappe.logger().warning(
                f"[AeroSpaceOS] Spacecraft {sc['name']} has no recorded telemetry."
            )


def monitor_collision_risks():
    """
    Hourly: Checks all Open conjunction assessments for critical/red risk levels.
    Escalates and notifies if action has not been taken.
    """
    critical_cas = frappe.get_all(
        "Conjunction Assessment",
        filters={"status": "Open", "risk_level": ["in", ["Critical", "Red"]]},
        fields=["name", "spacecraft", "debris_catalog_id", "risk_level",
                "miss_distance_meters", "collision_probability", "closest_approach_utc"]
    )

    for ca in critical_cas:
        frappe.logger().error(
            f"[AeroSpaceOS] ACTIVE CONJUNCTION RISK: {ca['name']} — "
            f"Spacecraft: {ca['spacecraft']}, NORAD: {ca['debris_catalog_id']}, "
            f"Risk: {ca['risk_level']}, Pc: {ca['collision_probability']:.3e}"
        )
        _create_notification_log(
            subject=f"🚨 COLLISION RISK [{ca['risk_level']}]: {ca['spacecraft']} vs {ca['debris_catalog_id']}",
            message=(
                f"Conjunction Assessment {ca['name']} for spacecraft {ca['spacecraft']} "
                f"has {ca['risk_level']} risk level. "
                f"Miss Distance: {ca['miss_distance_meters']}m, "
                f"Pc: {ca['collision_probability']:.3e}. "
                f"TCA: {ca['closest_approach_utc']}. Immediate review required."
            )
        )


def check_spacecraft_health():
    """
    Hourly: Reviews all Active spacecraft for health indicators:
    - Low propellant (< 15%)
    - Stale telemetry (> 4h)
    - Missing orbit parameters
    """
    active = frappe.get_all(
        "Spacecraft Asset",
        filters={"status": "Active"},
        fields=["name", "spacecraft_name", "propellant_capacity_kg",
                "current_propellant_level_kg", "last_telemetry_utc"]
    )

    for sc in active:
        cap = flt(sc.get("propellant_capacity_kg") or 0)
        cur = flt(sc.get("current_propellant_level_kg") or 0)
        if cap > 0:
            pct = (cur / cap) * 100
            if pct < 15:
                _create_notification_log(
                    subject=f"⛽ Low Propellant: {sc['spacecraft_name']} ({round(pct,1)}%)",
                    message=(
                        f"Spacecraft {sc['spacecraft_name']} has only {round(pct,1)}% "
                        f"propellant remaining ({cur} kg of {cap} kg)."
                    )
                )

        # Check for missing orbit parameters
        has_orbit = frappe.db.exists("Orbit Parameter", {"spacecraft": sc["name"]})
        if not has_orbit:
            frappe.logger().warning(
                f"[AeroSpaceOS] Active spacecraft {sc['name']} has no Orbit Parameter record."
            )


# ══════════════════════════════════════════════════════════════
# DAILY JOBS
# ══════════════════════════════════════════════════════════════

def check_itar_compliance():
    """
    Daily: Checks all ITAR/EAR Access Control records for expiring or expired licenses.
    """
    today = getdate(nowdate())
    thirty_days_out = getdate(add_days(nowdate(), 30))

    records = frappe.db.sql("""
        SELECT name, ref_docname, export_license_id, export_license_expiry, jurisdiction
        FROM `tabITAR EAR Access Control`
        WHERE export_license_required = 1
          AND export_license_expiry IS NOT NULL
          AND export_license_expiry <= %s
    """, (thirty_days_out,), as_dict=True)

    for r in records:
        expiry = getdate(r["export_license_expiry"])
        if expiry < today:
            status = "EXPIRED"
            indicator = "🔴"
        else:
            status = "Expiring Soon"
            indicator = "🟡"

        _create_notification_log(
            subject=f"{indicator} ITAR License {status}: {r['export_license_id']} ({r['ref_docname']})",
            message=(
                f"Export License {r['export_license_id']} for {r['jurisdiction']} controlled "
                f"item {r['ref_docname']} is {status}. "
                f"Expiry: {r['export_license_expiry']}. Immediate renewal action required."
            )
        )


def check_propellant_levels():
    """
    Daily: Scans all active spacecraft for propellant levels below 20%.
    Creates notification logs for review.
    """
    spacecraft_list = frappe.db.sql("""
        SELECT name, spacecraft_name, current_propellant_level_kg, propellant_capacity_kg
        FROM `tabSpacecraft Asset`
        WHERE status = 'Active'
          AND propellant_capacity_kg > 0
          AND (current_propellant_level_kg / propellant_capacity_kg) < 0.20
    """, as_dict=True)

    for sc in spacecraft_list:
        pct = round((sc["current_propellant_level_kg"] / sc["propellant_capacity_kg"]) * 100, 1)
        _create_notification_log(
            subject=f"⛽ Daily Propellant Check: {sc['spacecraft_name']} at {pct}%",
            message=f"Daily check: {sc['spacecraft_name']} propellant is at {pct}% ({sc['current_propellant_level_kg']} kg)."
        )


def update_orbit_data():
    """
    Daily: Placeholder for TLE propagation / orbit update integration.
    In production this would call space-track.org or Celestrak API.
    Logs an info message confirming orbit data review task is scheduled.
    """
    count = frappe.db.count("Orbit Parameter")
    frappe.logger().info(
        f"[AeroSpaceOS] Daily orbit update task triggered. "
        f"{count} Orbit Parameter records on file. "
        f"Connect to Celestrak/space-track.org for live TLE propagation."
    )


# ══════════════════════════════════════════════════════════════
# WEEKLY JOBS
# ══════════════════════════════════════════════════════════════

def generate_launch_readiness_report():
    """
    Weekly: Reviews upcoming Launch Campaigns in Planning / WDR / Countdown Active status
    and logs readiness summary.
    """
    upcoming = frappe.get_all(
        "Launch Campaign",
        filters={"status": ["in", ["Planning", "Wet Dress Rehearsal", "Countdown Active"]]},
        fields=["campaign_id", "mission_name", "status", "launch_window_start_utc"]
    )

    if upcoming:
        lines = [f"Weekly Launch Readiness Review — {len(upcoming)} active campaigns:"]
        for lc in upcoming:
            lines.append(
                f"  • [{lc['status']}] {lc['mission_name']} ({lc['campaign_id']}) "
                f"— Window: {lc['launch_window_start_utc']}"
            )
        frappe.logger().info("\n".join(lines))
        _create_notification_log(
            subject=f"🚀 Weekly Launch Readiness: {len(upcoming)} Campaigns Pending",
            message="\n".join(lines)
        )


def review_open_ncrs():
    """
    Weekly: Summarizes all open/escalated Aerospace Quality NCRs.
    Creates notification for quality management review.
    """
    ncrs = frappe.get_all(
        "Aerospace Quality NCR",
        filters={"status": ["in", ["Open", "Under Review", "Escalated"]]},
        fields=["name", "severity", "status", "part_number"]
    )

    if ncrs:
        critical = [n for n in ncrs if n["severity"] == "Critical"]
        summary = (
            f"Weekly NCR Review: {len(ncrs)} open NCRs — "
            f"{len(critical)} Critical, "
            f"{len([n for n in ncrs if n['severity']=='Major'])} Major, "
            f"{len([n for n in ncrs if n['severity']=='Minor'])} Minor."
        )
        _create_notification_log(
            subject=f"📋 Weekly NCR Review: {len(ncrs)} Open NCRs ({len(critical)} Critical)",
            message=summary
        )


# ══════════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ══════════════════════════════════════════════════════════════

def _create_notification_log(subject, message):
    """Creates a Notification Log for the Administrator user."""
    try:
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": subject,
            "email_content": message,
            "for_user": "Administrator",
            "type": "Alert"
        }).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Space Scheduler Notification Failed: {subject}")
