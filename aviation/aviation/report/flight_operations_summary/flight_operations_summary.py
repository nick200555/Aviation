import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Flight Number"), "fieldname": "flight_number", "fieldtype": "Data", "width": 120},
        {"label": _("Aircraft"), "fieldname": "aircraft", "fieldtype": "Link", "options": "Aircraft", "width": 120},
        {"label": _("Flight Date"), "fieldname": "flight_date", "fieldtype": "Date", "width": 100},
        {"label": _("Departure"), "fieldname": "departure_airport", "fieldtype": "Link", "options": "Airport", "width": 100},
        {"label": _("Destination"), "fieldname": "destination_airport", "fieldtype": "Link", "options": "Airport", "width": 100},
        {"label": _("Block Time (Hrs)"), "fieldname": "block_time_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Flight Time (Hrs)"), "fieldname": "flight_time_hours", "fieldtype": "Float", "width": 120},
        {"label": _("Delay (min)"), "fieldname": "delay_minutes", "fieldtype": "Int", "width": 100},
        {"label": _("Delay Code"), "fieldname": "delay_code", "fieldtype": "Data", "width": 100},
        {"label": _("Fuel Used (kg)"), "fieldname": "fuel_used_kg", "fieldtype": "Float", "width": 120},
        {"label": _("Defect"), "fieldname": "defect_description", "fieldtype": "Data", "width": 200},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("aircraft"):
        conditions += " AND fo.aircraft = %(aircraft)s"
    if filters.get("from_date"):
        conditions += " AND fo.flight_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND fo.flight_date <= %(to_date)s"
    if filters.get("departure_airport"):
        conditions += " AND fo.departure_airport = %(departure_airport)s"

    return frappe.db.sql(f"""
        SELECT
            fo.flight_number,
            fo.aircraft,
            fo.flight_date,
            fo.departure_airport,
            fo.destination_airport,
            fo.block_time_hours,
            fo.flight_time_hours,
            fo.delay_minutes,
            fo.delay_code,
            fo.fuel_used_kg,
            fo.defect_description
        FROM `tabFlight Operation` fo
        WHERE fo.docstatus = 1 {conditions}
        ORDER BY fo.flight_date DESC, fo.flight_number
    """, filters, as_dict=1)
