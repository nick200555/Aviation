# Copyright (c) 2024, Aviation Team and contributors
import frappe

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "CA ID", "fieldname": "name", "fieldtype": "Link",
         "options": "Conjunction Assessment", "width": 120},
        {"label": "Spacecraft", "fieldname": "spacecraft", "fieldtype": "Link",
         "options": "Spacecraft Asset", "width": 140},
        {"label": "Debris NORAD ID", "fieldname": "debris_catalog_id", "fieldtype": "Data", "width": 120},
        {"label": "TCA (UTC)", "fieldname": "closest_approach_utc", "fieldtype": "Datetime", "width": 150},
        {"label": "Miss Distance (m)", "fieldname": "miss_distance_meters", "fieldtype": "Float", "width": 130},
        {"label": "Collision Pc", "fieldname": "collision_probability", "fieldtype": "Float", "width": 120},
        {"label": "Risk Level", "fieldname": "risk_level", "fieldtype": "Data", "width": 90},
        {"label": "Action Req'd", "fieldname": "action_required", "fieldtype": "Check", "width": 90},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
        {"label": "Delta-V Req'd (m/s)", "fieldname": "delta_v_required_mps", "fieldtype": "Float", "width": 130},
    ]

    conditions = "1=1"
    if filters.get("spacecraft"):
        conditions += " AND spacecraft = %(spacecraft)s"
    if filters.get("risk_level"):
        conditions += " AND risk_level = %(risk_level)s"
    if filters.get("status"):
        conditions += " AND status = %(status)s"

    data = frappe.db.sql(f"""
        SELECT name, spacecraft, debris_catalog_id, closest_approach_utc,
               miss_distance_meters, collision_probability, risk_level,
               action_required, status, delta_v_required_mps
        FROM `tabConjunction Assessment`
        WHERE {conditions}
        ORDER BY closest_approach_utc ASC, collision_probability DESC
    """, filters, as_dict=True)

    return columns, data
