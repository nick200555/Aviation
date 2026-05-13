frappe.ui.form.on("Aircraft", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("View Certificates"), function() {
                frappe.set_route("List", "Aircraft Certificate", {"aircraft": frm.doc.name});
            }, __("Actions"));
            frm.add_custom_button(__("View Work Orders"), function() {
                frappe.set_route("List", "Maintenance Work Order", {"aircraft": frm.doc.name});
            }, __("Actions"));
            frm.add_custom_button(__("View AD Compliance"), function() {
                frappe.set_route("List", "AD Compliance Record", {"aircraft": frm.doc.name});
            }, __("Actions"));
            frm.add_custom_button(__("Log Flight Operation"), function() {
                frappe.new_doc("Flight Operation", {"aircraft": frm.doc.name});
            }, __("Create"));
        }
        // Show AOG indicator
        if (frm.doc.status === "AOG") {
            frm.dashboard.set_headline(__("Aircraft is AOG - Not Available for Operations"), "red");
        }
    }
});
