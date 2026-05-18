frappe.query_reports["Propellant Usage Report"] = {
    filters: [
        {fieldname: "launch_campaign", label: __("Launch Campaign"), fieldtype: "Link", options: "Launch Campaign"},
        {fieldname: "propellant_type", label: __("Propellant Type"), fieldtype: "Select",
         options: "\nLiquid Oxygen (LOX)\nLiquid Hydrogen (LH2)\nRP-1 Rocket Kerosene\nLiquid Methane (LCH4)\nHydrazine\nXenon Gas"}
    ]
};
