import frappe

@frappe.whitelist()
def get_maintenance_due(aircraft=None, days_ahead=30):
    """Returns maintenance items coming due."""
    from frappe.utils import today, add_days
    due_cutoff = add_days(today(), int(days_ahead))

    filters = {"docstatus": ["!=", 2], "status": ["not in", ["Completed", "Cancelled"]]}
    if aircraft:
        filters["aircraft"] = aircraft
    filters["planned_completion_date"] = ["<=", due_cutoff]

    return frappe.get_all(
        "Maintenance Work Order",
        filters=filters,
        fields=["name", "aircraft", "maintenance_type", "planned_completion_date", "status", "priority"],
        order_by="planned_completion_date asc"
    )

@frappe.whitelist()
def get_ad_compliance_summary(aircraft=None):
    """Returns AD compliance summary for fleet or specific aircraft."""
    filters = {"docstatus": 1}
    if aircraft:
        filters["aircraft"] = aircraft

    records = frappe.get_all(
        "AD Compliance Record",
        filters=filters,
        fields=["aircraft", "airworthiness_directive", "compliance_status", "next_due_date", "next_due_tah"]
    )
    pending = [r for r in records if r.compliance_status == "Pending"]
    overdue = [r for r in records if r.compliance_status == "Not Complied"]
    return {
        "total": len(records),
        "pending": len(pending),
        "overdue": len(overdue),
        "pending_items": pending,
        "overdue_items": overdue
    }
