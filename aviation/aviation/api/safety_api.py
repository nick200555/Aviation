import frappe

@frappe.whitelist(allow_guest=True)
def submit_safety_report(occurrence_date, occurrence_type, severity, summary, narrative=None, aircraft=None, reported_by=None):
    """External API to submit safety reports."""
    try:
        doc = frappe.get_doc({
            "doctype": "Safety Occurrence Report",
            "occurrence_date": occurrence_date,
            "occurrence_type": occurrence_type,
            "severity": severity,
            "summary": summary,
            "narrative": narrative,
            "aircraft": aircraft,
            "reported_by": reported_by or "Guest",
            "status": "Draft"
        })
        doc.insert(ignore_permissions=True)
        return {"status": "success", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Safety API Error")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def get_safety_stats():
    """Returns summary statistics for safety dashboard."""
    stats = frappe.db.sql("""
        SELECT severity, COUNT(*) as count
        FROM `tabSafety Occurrence Report`
        WHERE docstatus != 2
        GROUP BY severity
    """, as_dict=1)
    return stats
