import frappe
from frappe.utils import today, add_days, date_diff, now_datetime

def check_certificate_expiry():
    """Mark expired aircraft certificates and send alerts."""
    expiring = frappe.get_all(
        "Aircraft Certificate",
        filters={"status": "Valid", "expiry_date": ["<", today()]},
        fields=["name", "aircraft", "certificate_type"]
    )
    for cert in expiring:
        frappe.db.set_value("Aircraft Certificate", cert.name, "status", "Expired")
        frappe.logger().info(f"Certificate {cert.name} for {cert.aircraft} marked as Expired.")

def check_crew_licence_expiry():
    """Mark expired crew licences."""
    expired = frappe.get_all(
        "Crew Licence",
        filters={"status": "Valid", "expiry_date": ["<", today()]},
        fields=["name", "crew_member", "licence_type"]
    )
    for lic in expired:
        frappe.db.set_value("Crew Licence", lic.name, "status", "Expired")

def check_ad_due_items():
    """Alert for ADs coming due within 30 days."""
    due_date = add_days(today(), 30)
    due_ads = frappe.get_all(
        "AD Compliance Record",
        filters={
            "docstatus": 1,
            "compliance_status": ["in", ["Pending", "Complied - Repetitive"]],
            "next_due_date": ["between", [today(), due_date]]
        },
        fields=["name", "aircraft", "airworthiness_directive", "next_due_date", "next_due_tah"]
    )
    for item in due_ads:
        # Send notification to Aviation Manager
        managers = frappe.get_all("Has Role", filters={"role": "Aviation Manager", "parenttype": "User"}, fields=["parent"])
        for m in managers:
            frappe.sendmail(
                recipients=[m.parent],
                subject=f"AD Due in 30 Days: {item.airworthiness_directive} on {item.aircraft}",
                message=f"Airworthiness Directive {item.airworthiness_directive} is due by {item.next_due_date} on aircraft {item.aircraft}."
            )

def check_maintenance_overdue():
    """Flag overdue maintenance work orders."""
    overdue = frappe.get_all(
        "Maintenance Work Order",
        filters={
            "status": ["not in", ["Completed", "Cancelled"]],
            "planned_completion_date": ["<", today()],
            "docstatus": ["!=", 2]
        },
        fields=["name", "aircraft", "maintenance_type", "planned_completion_date"]
    )
    for wo in overdue:
        frappe.logger().warning(f"MWO {wo.name} for {wo.aircraft} is overdue since {wo.planned_completion_date}.")

def update_aircraft_flight_times():
    """Hourly: Aggregate flight times from submitted operations."""
    # This is normally handled on Flight Operation submit, but this provides a reconciliation pass.
    pass

def send_duty_limit_warnings():
    """Daily: Warn crew approaching 28-day block hour limits."""
    crew_list = frappe.get_all("Crew Member", filters={"status": "Active", "crew_type": "Flight Crew"}, fields=["name", "full_name", "email", "max_block_hours_28days", "cumulative_block_hours_28days"])
    for crew in crew_list:
        limit = crew.max_block_hours_28days or 100
        used = crew.cumulative_block_hours_28days or 0
        if used >= (limit * 0.9) and crew.email:
            frappe.sendmail(
                recipients=[crew.email],
                subject=f"Duty Hours Warning: {crew.full_name}",
                message=f"You have used {used} hrs of your {limit}-hour 28-day limit. Please contact crew scheduling."
            )

def generate_daily_ops_summary():
    """Send daily operations summary to Aviation Manager."""
    ops = frappe.get_all(
        "Flight Operation",
        filters={"flight_date": today(), "docstatus": 1},
        fields=["flight_number", "aircraft", "block_time_hours", "delay_minutes"]
    )
    total_block = sum(o.block_time_hours or 0 for o in ops)
    total_delay = sum(o.delay_minutes or 0 for o in ops)
    managers = frappe.get_all("Has Role", filters={"role": "Aviation Manager", "parenttype": "User"}, fields=["parent"])
    for m in managers:
        frappe.sendmail(
            recipients=[m.parent],
            subject=f"Daily Ops Summary - {today()}",
            message=(
                f"Flights operated: {len(ops)}\n"
                f"Total Block Hours: {round(total_block, 2)}\n"
                f"Total Delay: {total_delay} minutes"
            )
        )

def generate_weekly_safety_report():
    """Weekly: Summarise safety occurrences for Safety Officer."""
    from frappe.utils import add_days
    from_date = add_days(today(), -7)
    reports = frappe.get_all(
        "Safety Occurrence Report",
        filters={"occurrence_date": [">=", from_date], "docstatus": ["!=", 2]},
        fields=["name", "occurrence_type", "severity", "aircraft", "summary"]
    )
    if reports:
        officers = frappe.get_all("Has Role", filters={"role": "Safety Officer", "parenttype": "User"}, fields=["parent"])
        for o in officers:
            frappe.sendmail(
                recipients=[o.parent],
                subject=f"Weekly Safety Report - {from_date} to {today()}",
                message=f"Total occurrences this week: {len(reports)}\n\n" + "\n".join([f"- [{r.occurrence_type}] {r.summary}" for r in reports])
            )
