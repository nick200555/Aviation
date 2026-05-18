frappe.query_reports["Spacecraft Utilization Report"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nIntegration\nPre-Launch\nActive\nDecommissioned\nDe-orbited"
        },
        {
            fieldname: "orbit_type",
            label: __("Orbit Type"),
            fieldtype: "Select",
            options: "\nLEO\nMEO\nGEO\nSun-Synchronous\nLunar\nInterplanetary\nHEO"
        },
        {
            fieldname: "spacecraft_type",
            label: __("Spacecraft Type"),
            fieldtype: "Select",
            options: "\nSatellite\nLaunch Vehicle Booster\nUpper Stage\nCrew Capsule\nSpace Station Module\nProbe"
        }
    ],
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "propellant_pct") {
            let pct = parseFloat(data.propellant_pct);
            if (pct < 15) {
                value = `<span style="color:red; font-weight:bold">${value}</span>`;
            } else if (pct < 30) {
                value = `<span style="color:orange">${value}</span>`;
            }
        }
        if (column.fieldname === "status" && data.status === "Active") {
            value = `<span style="color:green; font-weight:bold">${value}</span>`;
        }
        return value;
    }
};
