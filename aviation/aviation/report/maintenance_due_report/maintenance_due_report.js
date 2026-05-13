frappe.query_reports["Maintenance Due Report"] = {
    "filters": [
        {
            "fieldname": "aircraft",
            "label": __("Aircraft"),
            "fieldtype": "Link",
            "options": "Aircraft"
        },
        {
            "fieldname": "days_ahead",
            "label": __("Days Ahead"),
            "fieldtype": "Int",
            "default": 30
        }
    ]
};
