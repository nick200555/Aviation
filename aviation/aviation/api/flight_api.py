import frappe

@frappe.whitelist()
def get_flight_schedule(from_date=None, to_date=None, aircraft=None):
    """Returns flight schedule for a date range."""
    from frappe.utils import today, add_days
    filters = {"docstatus": ["!=", 2]}
    if from_date:
        filters["flight_date"] = [">=", from_date]
    if to_date:
        filters["flight_date"] = ["<=", to_date]
    if aircraft:
        filters["aircraft"] = aircraft

    return frappe.get_all(
        "Flight Plan",
        filters=filters,
        fields=["name", "flight_number", "aircraft", "flight_date", "departure_airport",
                "destination_airport", "etd_utc", "eta_utc", "status", "block_fuel_kg"],
        order_by="flight_date asc, etd_utc asc"
    )

@frappe.whitelist()
def get_daily_ops_summary(date=None):
    """Returns operations summary for a specific date."""
    from frappe.utils import today
    ops_date = date or today()

    ops = frappe.get_all(
        "Flight Operation",
        filters={"flight_date": ops_date, "docstatus": 1},
        fields=["aircraft", "flight_number", "departure_airport", "destination_airport",
                "block_time_hours", "delay_minutes", "fuel_used_kg"]
    )
    total_block = sum(o.block_time_hours or 0 for o in ops)
    total_delay = sum(o.delay_minutes or 0 for o in ops)
    return {
        "date": ops_date,
        "flights": ops,
        "total_flights": len(ops),
        "total_block_hours": round(total_block, 2),
        "total_delay_minutes": total_delay
    }
