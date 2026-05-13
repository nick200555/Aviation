import frappe
from frappe.model.document import Document

class AircraftType(Document):
    def validate(self):
        if self.max_landing_weight_kg and self.max_takeoff_weight_kg:
            if self.max_landing_weight_kg > self.max_takeoff_weight_kg:
                frappe.throw("Maximum Landing Weight cannot exceed Maximum Takeoff Weight.")
        if self.is_etops_capable and not self.etops_rating_minutes:
            frappe.throw("ETOPS Rating (minutes) is required for ETOPS-capable aircraft types.")
