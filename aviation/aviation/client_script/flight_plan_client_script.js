// Flight Plan client-side validations and auto-calculations
frappe.ui.form.on("Flight Plan", {
    etd_utc: function(frm) { calculate_eet(frm); },
    eta_utc: function(frm) { calculate_eet(frm); },
    trip_fuel_kg: function(frm) { calculate_total_fuel(frm); },
    contingency_fuel_kg: function(frm) { calculate_total_fuel(frm); },
    alternate_fuel_kg: function(frm) { calculate_total_fuel(frm); },
    final_reserve_fuel_kg: function(frm) { calculate_total_fuel(frm); },
    extra_fuel_kg: function(frm) { calculate_total_fuel(frm); },
    aircraft: function(frm) {
        if (frm.doc.aircraft) {
            frappe.db.get_value("Aircraft", frm.doc.aircraft, ["status", "aircraft_type"], function(r) {
                if (r && r.status === "AOG") {
                    frappe.msgprint({
                        message: __("WARNING: Aircraft {0} is currently AOG (Aircraft on Ground). Please select another aircraft.", [frm.doc.aircraft]),
                        title: "AOG Aircraft",
                        indicator: "red"
                    });
                }
            });
        }
    }
});

function calculate_eet(frm) {
    if (frm.doc.etd_utc && frm.doc.eta_utc) {
        var etd = moment(frm.doc.etd_utc);
        var eta = moment(frm.doc.eta_utc);
        var diff_hours = eta.diff(etd, "minutes") / 60;
        if (diff_hours > 0) {
            frm.set_value("eet_hours", Math.round(diff_hours * 100) / 100);
        }
    }
}

function calculate_total_fuel(frm) {
    var total = (frm.doc.trip_fuel_kg || 0) +
                (frm.doc.contingency_fuel_kg || 0) +
                (frm.doc.alternate_fuel_kg || 0) +
                (frm.doc.final_reserve_fuel_kg || 0) +
                (frm.doc.extra_fuel_kg || 0);
    frm.set_value("total_fuel_required_kg", Math.round(total * 100) / 100);
}
