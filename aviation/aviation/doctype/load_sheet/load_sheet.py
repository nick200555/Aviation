import frappe
from frappe.model.document import Document

class LoadSheet(Document):
    def validate(self):
        self.calculate_weights()
        self.check_weight_limits()
        self.check_cg_limits()

    def calculate_weights(self):
        payload = (
            (self.pax_weight_kg or 0) +
            (self.cabin_baggage_kg or 0) +
            (self.hold_baggage_kg or 0) +
            (self.cargo_kg or 0) +
            (self.mail_kg or 0)
        )
        self.zero_fuel_weight = (self.dry_operating_weight or 0) + payload
        self.take_off_weight = self.zero_fuel_weight + (self.take_off_fuel_kg or 0)
        self.landing_weight = self.take_off_weight - (self.trip_fuel_kg or 0)

    def check_weight_limits(self):
        errors = []
        if self.max_zero_fuel_weight and self.zero_fuel_weight > self.max_zero_fuel_weight:
            errors.append(f"ZFW {self.zero_fuel_weight} kg exceeds MZFW {self.max_zero_fuel_weight} kg.")
        if self.max_take_off_weight and self.take_off_weight > self.max_take_off_weight:
            errors.append(f"TOW {self.take_off_weight} kg exceeds MTOW {self.max_take_off_weight} kg.")
        if self.max_landing_weight and self.landing_weight > self.max_landing_weight:
            errors.append(f"LW {self.landing_weight} kg exceeds MLW {self.max_landing_weight} kg.")
        if errors:
            frappe.throw("\n".join(errors), title="Weight Limit Exceeded")

    def check_cg_limits(self):
        if self.cg_takeoff_percent and self.cg_fwd_limit and self.cg_aft_limit:
            if self.cg_takeoff_percent < self.cg_fwd_limit or self.cg_takeoff_percent > self.cg_aft_limit:
                frappe.throw(
                    f"CG at Takeoff ({self.cg_takeoff_percent}% MAC) is outside limits "
                    f"[Fwd: {self.cg_fwd_limit}%, Aft: {self.cg_aft_limit}%]."
                )
