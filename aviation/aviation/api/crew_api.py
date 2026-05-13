import frappe

@frappe.whitelist()
def get_crew_availability(flight_date=None, aircraft_type=None):
    """Returns crew members available for duty on a given date."""
    from frappe.utils import today
    check_date = flight_date or today()

    # Crew with valid licences and no conflicting duty
    crew_list = frappe.get_all(
        "Crew Member",
        filters={"status": "Active", "crew_type": "Flight Crew"},
        fields=["name", "full_name", "crew_type", "base_airport", "cumulative_block_hours_28days", "max_block_hours_28days"]
    )

    available = []
    for crew in crew_list:
        # Check for conflicting duty on same day
        conflict = frappe.db.exists("Crew Duty Record", {
            "crew_member": crew.name,
            "duty_date": check_date,
            "docstatus": 1
        })
        if not conflict:
            # Check duty hours headroom
            headroom = (crew.max_block_hours_28days or 100) - (crew.cumulative_block_hours_28days or 0)
            crew["hours_headroom"] = round(headroom, 2)
            available.append(crew)

    return available

@frappe.whitelist()
def get_expiring_licences(days=60):
    """Returns crew licences expiring within specified days."""
    from frappe.utils import today, add_days
    return frappe.get_all(
        "Crew Licence",
        filters={
            "expiry_date": ["between", [today(), add_days(today(), int(days))]],
            "status": "Valid"
        },
        fields=["name", "crew_member", "licence_type", "licence_number", "expiry_date"],
        order_by="expiry_date asc"
    )
