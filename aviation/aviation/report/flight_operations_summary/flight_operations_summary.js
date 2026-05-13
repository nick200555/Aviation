frappe.query_reports["Flight Operations Summary"] = {
    "filters": [
        {
            "fieldname": "aircraft",
            "label": __("Aircraft"),
            "fieldtype": "Link",
            "options": "Aircraft"
        },
        {
            "fieldname": "departure_airport",
            "label": __("Departure Airport"),
            "fieldtype": "Link",
            "options": "Airport"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        }
    ]
};
