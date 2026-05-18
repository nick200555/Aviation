# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GroundStationPass(Document):
    def validate(self):
        self._validate_pass_times()

    def _validate_pass_times(self):
        if self.pass_start_utc and self.pass_end_utc:
            if self.pass_end_utc <= self.pass_start_utc:
                frappe.throw("Pass End must be after Pass Start.")

    def get_pass_duration_minutes(self):
        from frappe.utils import time_diff_in_seconds
        if self.pass_start_utc and self.pass_end_utc:
            seconds = time_diff_in_seconds(self.pass_end_utc, self.pass_start_utc)
            return round(seconds / 60, 2)
        return 0
