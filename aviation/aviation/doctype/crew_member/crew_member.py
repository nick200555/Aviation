import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, today

class CrewMember(Document):
    def validate(self):
        self.validate_age()
        self.validate_passport_expiry()

    def validate_age(self):
        if self.date_of_birth:
            age = date_diff(today(), self.date_of_birth) / 365
            if self.crew_type == "Flight Crew" and age > 65:
                frappe.msgprint(
                    f"Warning: {self.full_name} has reached the mandatory retirement age of 65 for flight crew.",
                    title="Age Limit Warning", indicator="orange"
                )

    def validate_passport_expiry(self):
        if self.passport_expiry and self.passport_expiry < today():
            frappe.msgprint(
                f"Warning: Passport for {self.full_name} has expired.",
                title="Passport Expired", indicator="red"
            )
