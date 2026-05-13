import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("ID"), "fieldname": "name", "fieldtype": "Link", "options": "Safety Occurrence Report", "width": 120},
        {"label": _("Date"), "fieldname": "occurrence_date", "fieldtype": "Date", "width": 100},
        {"label": _("Type"), "fieldname": "occurrence_type", "fieldtype": "Data", "width": 120},
        {"label": _("Severity"), "fieldname": "severity", "fieldtype": "Data", "width": 100},
        {"label": _("Aircraft"), "fieldname": "aircraft", "fieldtype": "Link", "options": "Aircraft", "width": 100},
        {"label": _("Summary"), "fieldname": "summary", "fieldtype": "Data", "width": 250},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("occurrence_type"):
        conditions += " AND occurrence_type = %(occurrence_type)s"
    if filters.get("severity"):
        conditions += " AND severity = %(severity)s"
    if filters.get("from_date"):
        conditions += " AND occurrence_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND occurrence_date <= %(to_date)s"

    return frappe.db.sql(f"""
        SELECT
            name,
            occurrence_date,
            occurrence_type,
            severity,
            aircraft,
            summary,
            status
        FROM `tabSafety Occurrence Report`
        WHERE docstatus != 2 {conditions}
        ORDER BY occurrence_date DESC
    """, filters, as_dict=1)
