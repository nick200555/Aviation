import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours

class FlightOperation(Document):
    def validate(self):
        self.calculate_times()
        self.calculate_fuel_used()

    def calculate_times(self):
        if self.off_block_utc and self.on_block_utc:
            self.block_time_hours = round(time_diff_in_hours(self.on_block_utc, self.off_block_utc), 2)
        if self.takeoff_utc and self.landing_utc:
            self.flight_time_hours = round(time_diff_in_hours(self.landing_utc, self.takeoff_utc), 2)

    def calculate_fuel_used(self):
        if self.fuel_on_departure_kg and self.fuel_on_arrival_kg:
            self.fuel_used_kg = self.fuel_on_departure_kg - self.fuel_on_arrival_kg

    def on_submit(self):
        self.update_aircraft_times()
        self.update_crew_duty_hours()

    def update_aircraft_times(self):
        aircraft = frappe.get_doc("Aircraft", self.aircraft)
        aircraft.total_airframe_hours = (aircraft.total_airframe_hours or 0) + (self.flight_time_hours or 0)
        aircraft.total_airframe_cycles = (aircraft.total_airframe_cycles or 0) + (self.number_of_landings or 1)
        aircraft.save(ignore_permissions=True)
        frappe.msgprint(f"Aircraft {self.aircraft} times updated: TAH={aircraft.total_airframe_hours}, TAC={aircraft.total_airframe_cycles}", alert=True)

    def update_crew_duty_hours(self):
        # Implementation for updating crew duty hours if needed,
        # usually handled by referencing this flight in a Crew Duty Record
        pass
