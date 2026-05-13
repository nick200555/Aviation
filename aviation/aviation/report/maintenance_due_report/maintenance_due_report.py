import frappe
from frappe import _
from frappe.utils import today, add_days

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Aircraft"), "fieldname": "aircraft", "fieldtype": "Link", "options": "Aircraft", "width": 120},
        {"label": _("Maintenance Type"), "fieldname": "maintenance_type", "fieldtype": "Data", "width": 150},
        {"label": _("Planned Start"), "fieldname": "planned_start_date", "fieldtype": "Date", "width": 100},
        {"label": _("Planned Completion"), "fieldname": "planned_completion_date", "fieldtype": "Date", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    conditions = "status NOT IN ('Completed', 'Cancelled')"
    if filters.get("aircraft"):
        conditions += " AND aircraft = %(aircraft)s"
    if filters.get("days_ahead"):
        due_cutoff = add_days(today(), int(filters.get("days_ahead")))
        conditions += f" AND planned_completion_date <= '{due_cutoff}'"

    return frappe.get_all(
        "Maintenance Work Order",
        filters=filters,
        fields=["aircraft", "maintenance_type", "planned_start_date", "planned_completion_date", "status", "priority"],
        order_by="planned_completion_date ASC"
    )
