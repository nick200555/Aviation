import frappe
from frappe.model.document import Document
from frappe.utils import today

class MaintenanceWorkOrder(Document):
    def validate(self):
        self.validate_dates()
        self.capture_aircraft_times()

    def validate_dates(self):
        if self.planned_start_date and self.planned_completion_date:
            if self.planned_completion_date < self.planned_start_date:
                frappe.throw("Planned Completion Date cannot be before Planned Start Date.")
        if self.actual_start_date and self.actual_completion_date:
            if self.actual_completion_date < self.actual_start_date:
                frappe.throw("Actual Completion Date cannot be before Actual Start Date.")

    def capture_aircraft_times(self):
        if not self.tah_at_induction and self.aircraft:
            aircraft = frappe.get_doc("Aircraft", self.aircraft)
            self.tah_at_induction = aircraft.total_airframe_hours
            self.tac_at_induction = aircraft.total_airframe_cycles

    def on_submit(self):
        if self.status == "Completed" and not self.release_to_service_by:
            frappe.throw("A LAME must be specified for Release to Service before the work order can be submitted as Completed.")
        frappe.db.set_value("Aircraft", self.aircraft, "status", "Scheduled Maintenance")

    def on_cancel(self):
        frappe.db.set_value("Aircraft", self.aircraft, "status", "Active")
