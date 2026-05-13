# Server Script: Validate Crew Duty Limits
# Trigger: Before Save on Crew Duty Record

import frappe
from frappe.utils import time_diff_in_hours, add_days, today

doc = frappe.get_doc(frappe.form_dict.get("doc"))

if doc.crew_member and doc.duty_start_utc and doc.duty_end_utc:
    crew = frappe.get_doc("Crew Member", doc.crew_member)

    # Check 28-day rolling block hours
    from_date = add_days(doc.duty_date, -28)
    total_28days = frappe.db.sql("""
        SELECT SUM(block_hours)
        FROM `tabCrew Duty Record`
        WHERE crew_member = %s
          AND duty_date BETWEEN %s AND %s
          AND docstatus = 1
          AND name != %s
    """, (doc.crew_member, from_date, doc.duty_date, doc.name or ""))[0][0] or 0

    projected = total_28days + (doc.block_hours or 0)
    limit = crew.max_block_hours_28days or 100

    if projected > limit:
        frappe.throw(
            f"Adding this duty would bring {crew.full_name}'s 28-day block hours to "
            f"{round(projected, 2)} hrs, exceeding the limit of {limit} hrs."
        )
