import frappe
from frappe import _

@frappe.whitelist()
def get_aircraft_status(airline=None):
    """Returns fleet status summary for dashboards."""
    filters = {}
    if airline:
        filters["airline"] = airline

    aircraft_list = frappe.get_all(
        "Aircraft",
        filters=filters,
        fields=["name", "aircraft_type", "status", "total_airframe_hours", "total_airframe_cycles"]
    )
    status_counts = {}
    for a in aircraft_list:
        status_counts[a.status] = status_counts.get(a.status, 0) + 1

    return {
        "aircraft": aircraft_list,
        "status_summary": status_counts,
        "total": len(aircraft_list)
    }

@frappe.whitelist()
def get_expiring_certificates(days=60):
    """Returns certificates expiring within specified days."""
    from frappe.utils import today, add_days
    return frappe.get_all(
        "Aircraft Certificate",
        filters={
            "expiry_date": ["between", [today(), add_days(today(), int(days))]],
            "status": "Valid"
        },
        fields=["name", "aircraft", "certificate_type", "expiry_date", "issuing_authority"],
        order_by="expiry_date asc"
    )
