# Copyright (c) 2024, Aviation Team and contributors
import frappe

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Campaign ID", "fieldname": "campaign_id", "fieldtype": "Link",
         "options": "Launch Campaign", "width": 120},
        {"label": "Mission Name", "fieldname": "mission_name", "fieldtype": "Data", "width": 160},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
        {"label": "Launch Vehicle", "fieldname": "launch_vehicle_booster", "fieldtype": "Data", "width": 130},
        {"label": "Primary Payload", "fieldname": "primary_payload", "fieldtype": "Link",
         "options": "Spacecraft Asset", "width": 140},
        {"label": "Launch Window Open", "fieldname": "launch_window_start_utc", "fieldtype": "Datetime", "width": 160},
        {"label": "Launch Window Close", "fieldname": "launch_window_end_utc", "fieldtype": "Datetime", "width": 160},
        {"label": "Actual Launch", "fieldname": "actual_launch_utc", "fieldtype": "Datetime", "width": 150},
        {"label": "Checklist Items", "fieldname": "checklist_total", "fieldtype": "Int", "width": 100},
        {"label": "Complete", "fieldname": "checklist_complete", "fieldtype": "Int", "width": 80},
        {"label": "Completion %", "fieldname": "completion_pct", "fieldtype": "Percent", "width": 100},
    ]

    conditions = "lc.docstatus < 2"
    if filters.get("status"):
        conditions += " AND lc.status = %(status)s"

    data = frappe.db.sql(f"""
        SELECT
            lc.campaign_id,
            lc.mission_name,
            lc.status,
            lc.launch_vehicle_booster,
            lc.primary_payload,
            lc.launch_window_start_utc,
            lc.launch_window_end_utc,
            lc.actual_launch_utc,
            COUNT(cl.name) AS checklist_total,
            SUM(CASE WHEN cl.status = 'Complete' THEN 1 ELSE 0 END) AS checklist_complete,
            CASE
                WHEN COUNT(cl.name) > 0
                THEN ROUND(SUM(CASE WHEN cl.status = 'Complete' THEN 1 ELSE 0 END) * 100.0 / COUNT(cl.name), 1)
                ELSE 0
            END AS completion_pct
        FROM `tabLaunch Campaign` lc
        LEFT JOIN `tabLaunch Countdown Checklist` cl ON cl.parent = lc.name
        WHERE {conditions}
        GROUP BY lc.name
        ORDER BY lc.launch_window_start_utc ASC
    """, filters, as_dict=True)

    return columns, data
