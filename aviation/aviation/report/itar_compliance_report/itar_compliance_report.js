frappe.query_reports["ITAR Compliance Report"] = {
    filters: [],
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "license_status") {
            if (data.license_status === "EXPIRED") value = `<span style="color:red;font-weight:bold">${value}</span>`;
            else if (data.license_status === "Expiring Soon") value = `<span style="color:orange">${value}</span>`;
            else if (data.license_status === "Valid") value = `<span style="color:green">${value}</span>`;
        }
        return value;
    }
};
