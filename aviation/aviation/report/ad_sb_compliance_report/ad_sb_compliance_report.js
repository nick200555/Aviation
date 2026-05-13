frappe.query_reports["AD SB Compliance Report"] = {
    "filters": [
        {
            "fieldname": "aircraft",
            "label": __("Aircraft"),
            "fieldtype": "Link",
            "options": "Aircraft"
        },
        {
            "fieldname": "compliance_status",
            "label": __("Compliance Status"),
            "fieldtype": "Select",
            "options": "\nPending\nComplied - Terminating\nComplied - Repetitive\nDeferred\nNot Complied"
        }
    ]
};
