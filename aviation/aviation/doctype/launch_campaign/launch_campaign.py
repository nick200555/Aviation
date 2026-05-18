# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class LaunchCampaign(Document):
    def validate(self):
        self._validate_launch_window()
        self._validate_booster_status()

    def _validate_launch_window(self):
        if self.launch_window_start_utc and self.launch_window_end_utc:
            if self.launch_window_end_utc <= self.launch_window_start_utc:
                frappe.throw("Launch Window Close must be after Launch Window Open.")

    def _validate_booster_status(self):
        if self.launch_vehicle_booster:
            booster = frappe.get_doc("Launch Vehicle Component", self.launch_vehicle_booster)
            if booster.status not in ["Ready for Flight"]:
                frappe.msgprint(
                    f"⚠️ Booster {self.launch_vehicle_booster} status is '{booster.status}'. "
                    f"It should be 'Ready for Flight' before launch.",
                    indicator="orange",
                    alert=True
                )

    def on_submit(self):
        if self.status not in ["Launched"]:
            frappe.throw("Cannot submit a Launch Campaign unless status is 'Launched'.")
        self._update_spacecraft_status()

    def _update_spacecraft_status(self):
        if self.primary_payload:
            frappe.db.set_value("Spacecraft Asset", self.primary_payload, "status", "Active")
            frappe.msgprint(f"✅ Spacecraft {self.primary_payload} status updated to Active.")

    def on_cancel(self):
        self.status = "Scrubbed"
        self.db_set("status", "Scrubbed")

    def get_checklist_completion(self):
        total = len(self.countdown_checklist)
        if total == 0:
            return 0
        completed = sum(1 for item in self.countdown_checklist if item.status == "Complete")
        return round((completed / total) * 100, 1)
