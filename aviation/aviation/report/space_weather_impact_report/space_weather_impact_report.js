frappe.query_reports["Space Weather Impact Report"] = {
    filters: [
        {fieldname: "solar_flare_class", label: __("Solar Flare Class"), fieldtype: "Select",
         options: "\nA-Class\nB-Class\nC-Class\nM-Class\nX-Class"}
    ]
};
