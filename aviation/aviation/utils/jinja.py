import frappe
from frappe.utils import today, date_diff

def get_aircraft_status(aircraft_name):
    """Returns status badge string for use in print formats."""
    status = frappe.db.get_value("Aircraft", aircraft_name, "status")
    return status or "Unknown"

def get_crew_duty_remaining(crew_member_name):
    """Returns remaining FDP hours for a crew member."""
    crew = frappe.get_doc("Crew Member", crew_member_name)
    limit = crew.max_block_hours_28days or 100
    used = crew.cumulative_block_hours_28days or 0
    return round(limit - used, 2)

def format_flight_time(decimal_hours):
    """Converts decimal hours to HH:MM format."""
    if decimal_hours is None:
        return "00:00"
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"
