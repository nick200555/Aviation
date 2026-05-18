# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

# NOAA Kp-index severity scale
KP_SEVERE = 7    # G3 - Severe geomagnetic storm
KP_EXTREME = 8   # G4 - Extreme
KP_MODERATE = 5  # G1/G2 Moderate


class SpaceWeatherAlert(Document):
    def validate(self):
        self._validate_kp_index()
        self._auto_suggest_action()

    def _validate_kp_index(self):
        if self.geomagnetic_storm_kp_index is not None:
            if not (0 <= self.geomagnetic_storm_kp_index <= 9):
                frappe.throw("Kp Index must be between 0 and 9.")

    def _auto_suggest_action(self):
        """Auto-suggest protective action based on storm severity."""
        kp = self.geomagnetic_storm_kp_index or 0
        flare = self.solar_flare_class or ""

        if kp >= KP_EXTREME or flare in ["X-Class"]:
            if not self.action_taken or self.action_taken == "None":
                self.action_taken = "Safe Mode Triggered"
                frappe.msgprint(
                    f"🌞 EXTREME Space Weather Event detected (Kp={kp}, Flare={flare}). "
                    f"Auto-setting action to 'Safe Mode Triggered'.",
                    indicator="red",
                    alert=True
                )
        elif kp >= KP_SEVERE or flare in ["M-Class"]:
            if not self.action_taken or self.action_taken == "None":
                self.action_taken = "Battery Charging Optimized"

    def after_insert(self):
        """Notify Safety Officer on new critical space weather events."""
        kp = self.geomagnetic_storm_kp_index or 0
        flare = self.solar_flare_class or ""
        if kp >= KP_SEVERE or flare in ["X-Class", "M-Class"]:
            frappe.get_doc({
                "doctype": "Notification Log",
                "subject": f"🌞 Space Weather Alert: {flare} Solar Flare, Kp={kp}",
                "email_content": f"A significant space weather event has been logged at {self.alert_utc}. "
                                 f"Solar Flare Class: {flare}, Kp Index: {kp}. "
                                 f"Action taken: {self.action_taken}. Review affected satellites.",
                "for_user": "Administrator",
                "type": "Alert"
            }).insert(ignore_permissions=True)
