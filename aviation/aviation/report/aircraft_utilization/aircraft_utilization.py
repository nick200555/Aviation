import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Aircraft"), "fieldname": "aircraft", "fieldtype": "Link", "options": "Aircraft", "width": 120},
        {"label": _("Type"), "fieldname": "aircraft_type", "fieldtype": "Link", "options": "Aircraft Type", "width": 100},
        {"label": _("Flight Date"), "fieldname": "flight_date", "fieldtype": "Date", "width": 100},
        {"label": _("Block Time (Hrs)"), "fieldname": "block_time_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Flight Time (Hrs)"), "fieldname": "flight_time_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Fuel Used (kg)"), "fieldname": "fuel_used_kg", "fieldtype": "Float", "width": 120},
        {"label": _("Number of Landings"), "fieldname": "number_of_landings", "fieldtype": "Int", "width": 120}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("aircraft"):
        conditions += " AND fo.aircraft = %(aircraft)s"
    if filters.get("from_date"):
        conditions += " AND fo.flight_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND fo.flight_date <= %(to_date)s"

    return frappe.db.sql(f"""
        SELECT
            fo.aircraft,
            a.aircraft_type,
            fo.flight_date,
            fo.block_time_hours,
            fo.flight_time_hours,
            fo.fuel_used_kg,
            fo.number_of_landings
        FROM `tabFlight Operation` fo
        JOIN `tabAircraft` a ON fo.aircraft = a.name
        WHERE fo.docstatus = 1 {conditions}
        ORDER BY fo.flight_date DESC
    """, filters, as_dict=1)
