# Server Script: Auto Update Aircraft Status
# Trigger: After Save on Maintenance Work Order

doc = frappe.get_doc(frappe.form_dict.get("doc"))

if doc.status == "In Progress" and doc.aircraft:
    frappe.db.set_value("Aircraft", doc.aircraft, "status", "Unscheduled Maintenance")
elif doc.status == "Completed" and doc.aircraft:
    frappe.db.set_value("Aircraft", doc.aircraft, "status", "Active")
    frappe.msgprint(f"Aircraft {doc.aircraft} has been returned to Active status.", alert=True)
