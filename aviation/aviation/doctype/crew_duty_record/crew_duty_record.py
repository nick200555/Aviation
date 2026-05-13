import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours

class CrewDutyRecord(Document):
    def validate(self):
        self.calculate_fdp()
        self.check_duty_limits()

    def calculate_fdp(self):
        if self.duty_start_utc and self.duty_end_utc:
            self.fdp_hours = round(time_diff_in_hours(self.duty_end_utc, self.duty_start_utc), 2)
            if self.fdp_hours < 0:
                frappe.throw("Duty End must be after Duty Start.")

    def check_duty_limits(self):
        if self.crew_member and self.fdp_hours:
            crew = frappe.get_doc("Crew Member", self.crew_member)
            if self.fdp_hours > (crew.max_fdp_hours or 13):
                self.fdp_exceeded = 1
                if not self.extension_approved:
                    frappe.msgprint(
                        f"Warning: FDP of {self.fdp_hours} hrs exceeds limit of {crew.max_fdp_hours} hrs for {crew.full_name}. "
                        "An extension approval is required.",
                        title="FDP Limit Exceeded", indicator="red"
                    )
            else:
                self.fdp_exceeded = 0
