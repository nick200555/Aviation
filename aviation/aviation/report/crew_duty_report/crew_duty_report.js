frappe.query_reports["Crew Duty Report"] = {
    "filters": [
        {
            "fieldname": "crew_member",
            "label": __("Crew Member"),
            "fieldtype": "Link",
            "options": "Crew Member"
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
