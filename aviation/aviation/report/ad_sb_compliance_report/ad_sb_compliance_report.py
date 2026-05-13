import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Aircraft"), "fieldname": "aircraft", "fieldtype": "Link", "options": "Aircraft", "width": 120},
        {"label": _("AD Number"), "fieldname": "airworthiness_directive", "fieldtype": "Link", "options": "Airworthiness Directive", "width": 150},
        {"label": _("Status"), "fieldname": "compliance_status", "fieldtype": "Data", "width": 120},
        {"label": _("Compliance Date"), "fieldname": "compliance_date", "fieldtype": "Date", "width": 100},
        {"label": _("Next Due Date"), "fieldname": "next_due_date", "fieldtype": "Date", "width": 100},
        {"label": _("Next Due TAH"), "fieldname": "next_due_tah", "fieldtype": "Float", "width": 120}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("aircraft"):
        conditions += " AND aircraft = %(aircraft)s"
    if filters.get("compliance_status"):
        conditions += " AND compliance_status = %(compliance_status)s"

    return frappe.db.sql(f"""
        SELECT
            aircraft,
            airworthiness_directive,
            compliance_status,
            compliance_date,
            next_due_date,
            next_due_tah
        FROM `tabAD Compliance Record`
        WHERE docstatus = 1 {conditions}
        ORDER BY next_due_date ASC
    """, filters, as_dict=1)
