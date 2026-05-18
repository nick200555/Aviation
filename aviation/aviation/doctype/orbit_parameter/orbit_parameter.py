# Copyright (c) 2024, Aviation Team and contributors
# For license information, please see license.txt

import frappe
import math
from frappe.model.document import Document

EARTH_RADIUS_KM = 6371.0
GM = 398600.4418  # Earth's gravitational parameter km^3/s^2


class OrbitParameter(Document):
    def validate(self):
        self._validate_eccentricity()
        self._auto_calculate_derived()

    def _validate_eccentricity(self):
        if self.eccentricity is not None:
            if self.eccentricity < 0 or self.eccentricity >= 1:
                frappe.throw("Eccentricity must be between 0 (circular) and < 1 (elliptical).")

    def _auto_calculate_derived(self):
        """Auto-calculate apogee, perigee, and orbital period from Keplerian elements."""
        if self.semi_major_axis_km and self.eccentricity is not None:
            a = self.semi_major_axis_km
            e = self.eccentricity

            # Apogee and Perigee altitudes above Earth surface
            self.apogee_km = round(a * (1 + e) - EARTH_RADIUS_KM, 3)
            self.perigee_km = round(a * (1 - e) - EARTH_RADIUS_KM, 3)

            # Orbital Period using Kepler's Third Law: T = 2π√(a³/GM)
            period_seconds = 2 * math.pi * math.sqrt((a ** 3) / GM)
            self.orbital_period_minutes = round(period_seconds / 60, 4)

            # Mean motion (revolutions per day)
            self.mean_motion_rev_per_day = round(86400 / period_seconds, 8)
