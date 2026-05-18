# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_seconds


class PropellantLoadLog(Document):
    def validate(self):
        self._calculate_variance()
        self._calculate_duration()
        self._validate_safety_clearance()

    def _calculate_variance(self):
        if self.actual_loaded_mass_kg and self.target_loading_mass_kg:
            self.loading_variance_kg = round(
                self.actual_loaded_mass_kg - self.target_loading_mass_kg, 3
            )

    def _calculate_duration(self):
        if self.loading_start_utc and self.loading_end_utc:
            seconds = time_diff_in_seconds(self.loading_end_utc, self.loading_start_utc)
            if seconds < 0:
                frappe.throw("Loading End UTC must be after Loading Start UTC.")
            self.loading_duration_minutes = round(seconds / 60, 2)

    def _validate_safety_clearance(self):
        if not self.safety_clearance:
            frappe.msgprint(
                "⚠️ Safety Clearance has NOT been confirmed. Ensure authorization before submission.",
                indicator="orange",
                alert=True
            )

    def on_submit(self):
        if not self.safety_clearance:
            frappe.throw("Cannot submit Propellant Load Log without Safety Clearance confirmation.")
        if not self.authorized_by:
            frappe.throw("Authorization must be set before submitting.")
