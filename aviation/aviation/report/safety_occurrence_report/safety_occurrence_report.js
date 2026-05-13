frappe.query_reports["Safety Occurrence Report"] = {
    "filters": [
        {
            "fieldname": "occurrence_type",
            "label": __("Occurrence Type"),
            "fieldtype": "Select",
            "options": "\nAccident\nSerious Incident\nIncident\nHazard\nVoluntary Report"
        },
        {
            "fieldname": "severity",
            "label": __("Severity"),
            "fieldtype": "Select",
            "options": "\nNegligible\nMinor\nModerate\nMajor\nCatastrophic"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -3)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        }
    ]
};
