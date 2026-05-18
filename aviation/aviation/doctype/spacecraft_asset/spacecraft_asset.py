# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SpacecraftAsset(Document):
    def validate(self):
        self._validate_propellant_levels()
        self._validate_lifetime()

    def _validate_propellant_levels(self):
        if self.propellant_capacity_kg and self.current_propellant_level_kg:
            if self.current_propellant_level_kg < 0:
                frappe.throw("Current Propellant Level cannot be negative.")
            if self.current_propellant_level_kg > self.propellant_capacity_kg:
                frappe.throw(
                    f"Current Propellant Level ({self.current_propellant_level_kg} kg) "
                    f"cannot exceed Capacity ({self.propellant_capacity_kg} kg)."
                )
            # Warn if propellant is below 15%
            pct = self.current_propellant_level_kg / self.propellant_capacity_kg
            if pct < 0.15:
                frappe.msgprint(
                    f"⚠️ Low propellant warning: {self.spacecraft_name} is at "
                    f"{round(pct * 100, 1)}% propellant.",
                    alert=True,
                    indicator="orange"
                )

    def _validate_lifetime(self):
        if self.estimated_lifetime_years and self.estimated_lifetime_years < 0:
            frappe.throw("Estimated Lifetime must be a positive number.")

    def after_insert(self):
        frappe.logger().info(f"Spacecraft Asset created: {self.spacecraft_id} — {self.spacecraft_name}")

    def on_update(self):
        self.last_telemetry_utc = now_datetime()
        self.db_set("last_telemetry_utc", self.last_telemetry_utc, update_modified=False)

    def get_propellant_percentage(self):
        if self.propellant_capacity_kg and self.propellant_capacity_kg > 0:
            return round((self.current_propellant_level_kg / self.propellant_capacity_kg) * 100, 2)
        return 0.0

    def trigger_low_propellant_alert(self):
        """Trigger notification if propellant is critically low."""
        pct = self.get_propellant_percentage()
        if pct < 10:
            frappe.get_doc({
                "doctype": "Notification Log",
                "subject": f"🛸 CRITICAL: {self.spacecraft_name} — Propellant at {pct}%",
                "email_content": f"Spacecraft {self.spacecraft_name} ({self.spacecraft_id}) has only {pct}% propellant remaining. Immediate ground contact required.",
                "for_user": "Administrator",
                "type": "Alert"
            }).insert(ignore_permissions=True)
