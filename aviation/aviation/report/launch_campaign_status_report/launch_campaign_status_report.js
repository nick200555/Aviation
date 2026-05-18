frappe.query_reports["Launch Campaign Status Report"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nPlanning\nWet Dress Rehearsal\nCountdown Active\nLaunched\nAborted\nScrubbed"
        }
    ]
};
