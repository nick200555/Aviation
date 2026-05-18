# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, add_days


class ItarEarAccessControl(Document):
    def validate(self):
        self._validate_license_expiry()
        self._validate_jurisdiction_fields()

    def _validate_license_expiry(self):
        if self.export_license_required and self.export_license_expiry:
            if getdate(self.export_license_expiry) < getdate(nowdate()):
                frappe.msgprint(
                    f"⚠️ Export License {self.export_license_id} has EXPIRED on "
                    f"{self.export_license_expiry}. Immediate renewal required.",
                    indicator="red",
                    alert=True
                )
            elif getdate(self.export_license_expiry) <= getdate(add_days(nowdate(), 30)):
                frappe.msgprint(
                    f"⚠️ Export License {self.export_license_id} expires in less than 30 days "
                    f"({self.export_license_expiry}). Please initiate renewal.",
                    indicator="orange",
                    alert=True
                )

    def _validate_jurisdiction_fields(self):
        if self.jurisdiction == "ITAR" and not self.usml_category:
            frappe.msgprint(
                "ITAR jurisdiction selected but no USML Category provided.",
                indicator="orange"
            )
        if self.jurisdiction == "EAR" and not self.eccn_number:
            frappe.msgprint(
                "EAR jurisdiction selected but no ECCN Number provided.",
                indicator="orange"
            )
