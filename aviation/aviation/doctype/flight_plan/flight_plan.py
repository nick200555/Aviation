import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours

class FlightPlan(Document):
    def validate(self):
        self.calculate_eet()
        self.calculate_total_fuel()
        self.validate_crew_assignments()

    def calculate_eet(self):
        if self.etd_utc and self.eta_utc:
            self.eet_hours = time_diff_in_hours(self.eta_utc, self.etd_utc)
            if self.eet_hours <= 0:
                frappe.throw("ETA must be after ETD.")

    def calculate_total_fuel(self):
        self.total_fuel_required_kg = (
            (self.trip_fuel_kg or 0) +
            (self.contingency_fuel_kg or 0) +
            (self.alternate_fuel_kg or 0) +
            (self.final_reserve_fuel_kg or 0) +
            (self.extra_fuel_kg or 0)
        )
        if self.block_fuel_kg and self.block_fuel_kg < self.total_fuel_required_kg:
            frappe.throw(
                f"Block Fuel ({self.block_fuel_kg} kg) is less than Total Fuel Required ({self.total_fuel_required_kg} kg). "
                "Check fuel plan."
            )

    def validate_crew_assignments(self):
        if not self.crew_assignments:
            frappe.throw("At least one crew member must be assigned to the flight.")
        captain_assigned = any(row.role == "Captain" for row in self.crew_assignments)
        if not captain_assigned:
            frappe.throw("A Captain must be assigned to the flight.")

    def on_submit(self):
        self.status = "Filed"
        self.db_set("status", "Filed")
        self.notify_crew()

    def notify_crew(self):
        for row in self.crew_assignments:
            crew = frappe.get_doc("Crew Member", row.crew_member)
            if crew.email:
                frappe.sendmail(
                    recipients=[crew.email],
                    subject=f"Flight Duty Notification: {self.flight_number} on {self.flight_date}",
                    message=f"You have been assigned as {row.role} for flight {self.flight_number} departing {self.departure_airport} on {self.flight_date}."
                )
