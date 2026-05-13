import frappe
from frappe.model.document import Document
from frappe.utils import today

class Aircraft(Document):
    def validate(self):
        if self.manufacture_date and self.entry_into_service_date:
            if self.entry_into_service_date < self.manufacture_date:
                frappe.throw("Entry into Service Date cannot be before Manufacture Date.")
        if self.total_airframe_hours and self.total_airframe_hours < 0:
            frappe.throw("Total Airframe Hours cannot be negative.")

    def after_insert(self):
        self.create_default_certificates()

    def create_default_certificates(self):
        """Auto-create Certificate of Airworthiness record on aircraft creation."""
        if not frappe.db.exists("Aircraft Certificate", {"aircraft": self.name, "certificate_type": "Certificate of Airworthiness"}):
            doc = frappe.new_doc("Aircraft Certificate")
            doc.aircraft = self.name
            doc.certificate_type = "Certificate of Airworthiness"
            doc.issuing_authority = "DGCA"
            doc.issue_date = today()
            doc.status = "Valid"
            doc.insert(ignore_permissions=True)
