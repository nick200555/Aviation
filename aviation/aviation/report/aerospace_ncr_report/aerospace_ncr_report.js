frappe.query_reports["Aerospace NCR Report"] = {
    filters: [
        {fieldname: "severity", label: __("Severity"), fieldtype: "Select",
         options: "\nMinor\nMajor\nCritical"},
        {fieldname: "status", label: __("Status"), fieldtype: "Select",
         options: "\nOpen\nUnder Review\nDispositioned\nClosed\nEscalated"}
    ],
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "severity") {
            const colors = {Critical: "red", Major: "orange", Minor: "gray"};
            if (colors[data.severity]) value = `<span style="color:${colors[data.severity]};font-weight:bold">${value}</span>`;
        }
        return value;
    }
};
