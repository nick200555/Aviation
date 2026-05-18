frappe.query_reports["Conjunction Risk Report"] = {
    filters: [
        {fieldname: "spacecraft", label: __("Spacecraft"), fieldtype: "Link", options: "Spacecraft Asset"},
        {fieldname: "risk_level", label: __("Risk Level"), fieldtype: "Select",
         options: "\nGreen\nYellow\nRed\nCritical"},
        {fieldname: "status", label: __("Status"), fieldtype: "Select",
         options: "\nOpen\nManeuver Planned\nManeuver Executed\nMonitored - Safe\nClosed"}
    ],
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "risk_level") {
            const colors = {Critical: "red", Red: "orange", Yellow: "#b8860b", Green: "green"};
            const color = colors[data.risk_level];
            if (color) value = `<span style="color:${color}; font-weight:bold">${value}</span>`;
        }
        return value;
    }
};
