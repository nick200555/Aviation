# Copyright (c) 2024, Aviation Team and contributors
import frappe

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Log ID", "fieldname": "name", "fieldtype": "Link",
         "options": "Propellant Load Log", "width": 120},
        {"label": "Campaign", "fieldname": "launch_campaign", "fieldtype": "Link",
         "options": "Launch Campaign", "width": 130},
        {"label": "Propellant Type", "fieldname": "propellant_type", "fieldtype": "Data", "width": 160},
        {"label": "Target (kg)", "fieldname": "target_loading_mass_kg", "fieldtype": "Float", "width": 100},
        {"label": "Actual (kg)", "fieldname": "actual_loaded_mass_kg", "fieldtype": "Float", "width": 100},
        {"label": "Variance (kg)", "fieldname": "loading_variance_kg", "fieldtype": "Float", "width": 100},
        {"label": "Cryo Temp (K)", "fieldname": "cryo_temperature_kelvin", "fieldtype": "Float", "width": 110},
        {"label": "Tank Pressure (PSI)", "fieldname": "tank_pressure_psi", "fieldtype": "Float", "width": 120},
        {"label": "Boil-off (kg/min)", "fieldname": "boil_off_rate_kg_min", "fieldtype": "Float", "width": 120},
        {"label": "Duration (min)", "fieldname": "loading_duration_minutes", "fieldtype": "Float", "width": 110},
        {"label": "Safety Cleared", "fieldname": "safety_clearance", "fieldtype": "Check", "width": 100},
    ]

    conditions = "docstatus < 2"
    if filters.get("launch_campaign"):
        conditions += " AND launch_campaign = %(launch_campaign)s"
    if filters.get("propellant_type"):
        conditions += " AND propellant_type = %(propellant_type)s"

    data = frappe.db.sql(f"""
        SELECT name, launch_campaign, propellant_type,
               target_loading_mass_kg, actual_loaded_mass_kg, loading_variance_kg,
               cryo_temperature_kelvin, tank_pressure_psi, boil_off_rate_kg_min,
               loading_duration_minutes, safety_clearance
        FROM `tabPropellant Load Log`
        WHERE {conditions}
        ORDER BY loading_start_utc DESC
    """, filters, as_dict=True)

    return columns, data
