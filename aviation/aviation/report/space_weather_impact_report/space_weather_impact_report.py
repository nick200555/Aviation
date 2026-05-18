# Copyright (c) 2024, Aviation Team and contributors
import frappe

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Alert ID", "fieldname": "name", "fieldtype": "Link",
         "options": "Space Weather Alert", "width": 120},
        {"label": "Alert Time (UTC)", "fieldname": "alert_utc", "fieldtype": "Datetime", "width": 150},
        {"label": "Solar Flare Class", "fieldname": "solar_flare_class", "fieldtype": "Data", "width": 120},
        {"label": "Kp Index", "fieldname": "geomagnetic_storm_kp_index", "fieldtype": "Int", "width": 90},
        {"label": "Solar Radiation (pfu)", "fieldname": "solar_radiation_level", "fieldtype": "Float", "width": 130},
        {"label": "Action Taken", "fieldname": "action_taken", "fieldtype": "Data", "width": 170},
        {"label": "Affected Satellites", "fieldname": "affected_count", "fieldtype": "Int", "width": 120},
    ]

    conditions = "1=1"
    if filters.get("solar_flare_class"):
        conditions += " AND swa.solar_flare_class = %(solar_flare_class)s"

    data = frappe.db.sql(f"""
        SELECT swa.name, swa.alert_utc, swa.solar_flare_class,
               swa.geomagnetic_storm_kp_index, swa.solar_radiation_level, swa.action_taken,
               COUNT(aff.name) AS affected_count
        FROM `tabSpace Weather Alert` swa
        LEFT JOIN `tabAffected Satellites` aff ON aff.parent = swa.name
        WHERE {conditions}
        GROUP BY swa.name
        ORDER BY swa.alert_utc DESC
    """, filters, as_dict=True)

    return columns, data
