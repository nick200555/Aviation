# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class AerospaceQualityNcr(Document):
    def validate(self):
        self._validate_capa_requirements()
        self._auto_escalate_critical()

    def _validate_capa_requirements(self):
        if self.severity in ["Major", "Critical"] and not self.corrective_and_preventive_action_required:
            frappe.msgprint(
                f"⚠️ NCR severity is '{self.severity}'. AS9100 requires CAPA for Major/Critical NCRs. "
                f"Please confirm CAPA requirement.",
                indicator="orange",
                alert=True
            )

    def _auto_escalate_critical(self):
        if self.severity == "Critical" and self.status == "Open":
            self.status = "Escalated"
            frappe.msgprint(
                "🚨 Critical NCR automatically escalated for immediate quality manager attention.",
                indicator="red",
                alert=True
            )

    def on_submit(self):
        if not self.quality_manager_signature:
            frappe.throw("Quality Manager sign-off is required before submitting an NCR.")
        if not self.disposition:
            frappe.throw("Disposition must be set before closing an NCR.")
        self.sign_off_date = nowdate()
        self.db_set("sign_off_date", self.sign_off_date)

    def on_cancel(self):
        self.status = "Closed"
        self.db_set("status", "Closed")
