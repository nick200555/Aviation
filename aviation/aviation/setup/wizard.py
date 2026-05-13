import frappe

def on_wizard_complete(args):
    """Called when the ERPNext setup wizard is completed."""
    # Auto-create a default Airline record using the company name
    company = args.get("company_name")
    if company:
        # Create a placeholder airline entry if none exists
        if not frappe.db.exists("Airline", {"airline_name": company}):
            try:
                doc = frappe.new_doc("Airline")
                doc.airline_name = company
                # Default ICAO designator: first 3 letters of company name, uppercased
                doc.icao_designator = company[:3].upper()
                doc.is_active = 1
                doc.insert()
                frappe.db.commit()
            except Exception:
                pass  # Don't block wizard completion if airline creation fails

    frappe.msgprint(
        "Aviation Management System setup complete. "
        "Please configure your Aircraft Types, Aircraft, and Airports to get started.",
        title="Aviation Setup",
        indicator="green"
    )
