import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Crew Member"), "fieldname": "crew_member", "fieldtype": "Link", "options": "Crew Member", "width": 150},
        {"label": _("Duty Date"), "fieldname": "duty_date", "fieldtype": "Date", "width": 100},
        {"label": _("Role"), "fieldname": "role_on_flight", "fieldtype": "Data", "width": 120},
        {"label": _("FDP (Hrs)"), "fieldname": "fdp_hours", "fieldtype": "Float", "width": 100},
        {"label": _("Block Time (Hrs)"), "fieldname": "block_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Extension?"), "fieldname": "extension_approved", "fieldtype": "Check", "width": 100}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("crew_member"):
        conditions += " AND crew_member = %(crew_member)s"
    if filters.get("from_date"):
        conditions += " AND duty_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND duty_date <= %(to_date)s"

    return frappe.db.sql(f"""
        SELECT
            crew_member,
            duty_date,
            role_on_flight,
            fdp_hours,
            block_hours,
            extension_approved
        FROM `tabCrew Duty Record`
        WHERE docstatus = 1 {conditions}
        ORDER BY duty_date DESC
    """, filters, as_dict=1)
