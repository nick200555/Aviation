import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, date_diff

class AircraftCertificate(Document):
    def validate(self):
        if self.expiry_date and self.issue_date:
            if self.expiry_date < self.issue_date:
                frappe.throw("Expiry Date cannot be before Issue Date.")
        self.auto_set_status()

    def auto_set_status(self):
        if self.expiry_date:
            days_to_expiry = date_diff(self.expiry_date, today())
            if days_to_expiry < 0:
                self.status = "Expired"
            elif self.status == "Expired" and days_to_expiry >= 0:
                self.status = "Valid"
