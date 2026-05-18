# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LaunchVehicleComponent(Document):
    def validate(self):
        self._validate_launch_count()
        self._check_max_reuses()

    def _validate_launch_count(self):
        if self.number_of_launches and self.number_of_launches < 0:
            frappe.throw("Number of Launches cannot be negative.")

    def _check_max_reuses(self):
        if self.max_reuses and self.number_of_launches:
            if self.number_of_launches >= self.max_reuses:
                frappe.msgprint(
                    f"⚠️ Component {self.component_id} has reached or exceeded its maximum "
                    f"approved reuses ({self.max_reuses}). Status should be reviewed.",
                    indicator="red",
                    alert=True
                )

    def before_save(self):
        if self.number_of_launches and self.max_reuses:
            if self.number_of_launches >= self.max_reuses and self.status == "Ready for Flight":
                frappe.throw(
                    f"Component {self.component_id} has exceeded max reuses. "
                    f"Cannot set status to 'Ready for Flight'."
                )
