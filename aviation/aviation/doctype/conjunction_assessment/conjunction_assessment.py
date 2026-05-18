# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

# ESA/NASA Conjunction Data Message (CDM) standard thresholds
PC_RED_THRESHOLD = 1e-4      # Pc > 1/10,000 = mandatory maneuver consideration
PC_YELLOW_THRESHOLD = 1e-5   # Pc > 1/100,000 = elevated concern
MISS_DISTANCE_CRITICAL_M = 500.0   # < 500m is Critical
MISS_DISTANCE_RED_M = 2000.0       # < 2km is Red


class ConjunctionAssessment(Document):
    def validate(self):
        self._auto_set_risk_level()
        self._auto_flag_action_required()

    def _auto_set_risk_level(self):
        """Auto-categorize risk level based on Pc and miss distance."""
        pc = self.collision_probability or 0
        md = self.miss_distance_meters or float("inf")

        if pc >= PC_RED_THRESHOLD or md <= MISS_DISTANCE_CRITICAL_M:
            self.risk_level = "Critical"
        elif pc >= PC_YELLOW_THRESHOLD or md <= MISS_DISTANCE_RED_M:
            self.risk_level = "Red"
        elif pc >= 1e-6:
            self.risk_level = "Yellow"
        else:
            self.risk_level = "Green"

    def _auto_flag_action_required(self):
        if self.risk_level in ["Red", "Critical"]:
            self.action_required = 1
            if not self.mitigation_maneuver_plan:
                frappe.msgprint(
                    f"🚨 CRITICAL conjunction detected for {self.spacecraft}! "
                    f"Pc={self.collision_probability}, Miss Distance={self.miss_distance_meters}m. "
                    f"Please provide a mitigation maneuver plan.",
                    indicator="red",
                    alert=True
                )

    def on_update(self):
        if self.status in ["Closed", "Monitored - Safe"] and not self.resolved_at:
            self.db_set("resolved_at", now_datetime())
            self.db_set("resolved_by", frappe.session.user)
