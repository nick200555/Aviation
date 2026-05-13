frappe.ui.form.on("Load Sheet", {
    pax_weight_kg: calculate_weights,
    cabin_baggage_kg: calculate_weights,
    hold_baggage_kg: calculate_weights,
    cargo_kg: calculate_weights,
    mail_kg: calculate_weights,
    dry_operating_weight: calculate_weights,
    take_off_fuel_kg: calculate_weights,
    trip_fuel_kg: calculate_weights
});

function calculate_weights(frm) {
    var payload = (frm.doc.pax_weight_kg || 0) +
                  (frm.doc.cabin_baggage_kg || 0) +
                  (frm.doc.hold_baggage_kg || 0) +
                  (frm.doc.cargo_kg || 0) +
                  (frm.doc.mail_kg || 0);
    var zfw = (frm.doc.dry_operating_weight || 0) + payload;
    var tow = zfw + (frm.doc.take_off_fuel_kg || 0);
    var lw = tow - (frm.doc.trip_fuel_kg || 0);
    frm.set_value("zero_fuel_weight", zfw);
    frm.set_value("take_off_weight", tow);
    frm.set_value("landing_weight", lw);

    // Weight limit colour indicators
    if (frm.doc.max_take_off_weight && tow > frm.doc.max_take_off_weight) {
        frappe.msgprint({message: __("TOW {0} kg EXCEEDS MTOW {1} kg!", [tow, frm.doc.max_take_off_weight]), indicator: "red", title: "Weight Limit Exceeded"});
    }
}
