import frappe
from frappe.model.document import Document

class SafetyOccurrenceReport(Document):
    def on_submit(self):
        # Notify stakeholders on submission
        pass
