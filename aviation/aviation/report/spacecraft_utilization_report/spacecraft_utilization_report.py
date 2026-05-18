# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Spacecraft ID", "fieldname": "spacecraft_id", "fieldtype": "Link",
         "options": "Spacecraft Asset", "width": 140},
        {"label": "Name", "fieldname": "spacecraft_name", "fieldtype": "Data", "width": 160},
        {"label": "Type", "fieldname": "spacecraft_type", "fieldtype": "Data", "width": 140},
        {"label": "Orbit", "fieldname": "orbit_type", "fieldtype": "Data", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Propellant Type", "fieldname": "propellant_type", "fieldtype": "Data", "width": 130},
        {"label": "Capacity (kg)", "fieldname": "propellant_capacity_kg", "fieldtype": "Float", "width": 110},
        {"label": "Current Level (kg)", "fieldname": "current_propellant_level_kg", "fieldtype": "Float", "width": 130},
        {"label": "Propellant %", "fieldname": "propellant_pct", "fieldtype": "Percent", "width": 100},
        {"label": "Delta-V Budget (m/s)", "fieldname": "delta_v_budget_mps", "fieldtype": "Float", "width": 130},
        {"label": "Battery (V)", "fieldname": "battery_voltage_v", "fieldtype": "Float", "width": 100},
        {"label": "Solar Power (W)", "fieldname": "solar_array_power_w", "fieldtype": "Float", "width": 110},
        {"label": "Last Telemetry", "fieldname": "last_telemetry_utc", "fieldtype": "Datetime", "width": 150},
        {"label": "Est. Lifetime (yr)", "fieldname": "estimated_lifetime_years", "fieldtype": "Float", "width": 120},
    ]

    conditions = "1=1"
    if filters.get("status"):
        conditions += f" AND status = %(status)s"
    if filters.get("orbit_type"):
        conditions += f" AND orbit_type = %(orbit_type)s"
    if filters.get("spacecraft_type"):
        conditions += f" AND spacecraft_type = %(spacecraft_type)s"

    data = frappe.db.sql(f"""
        SELECT
            spacecraft_id,
            spacecraft_name,
            spacecraft_type,
            orbit_type,
            status,
            propellant_type,
            propellant_capacity_kg,
            current_propellant_level_kg,
            CASE
                WHEN propellant_capacity_kg > 0
                THEN ROUND((current_propellant_level_kg / propellant_capacity_kg) * 100, 2)
                ELSE 0
            END AS propellant_pct,
            delta_v_budget_mps,
            battery_voltage_v,
            solar_array_power_w,
            last_telemetry_utc,
            estimated_lifetime_years
        FROM `tabSpacecraft Asset`
        WHERE {conditions}
        ORDER BY status, spacecraft_name
    """, filters, as_dict=True)

    return columns, data
