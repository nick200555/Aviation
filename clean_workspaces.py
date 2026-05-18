import frappe

def execute():
    # Delete the legacy workspaces that are cluttering the database
    for ws in ["Aviation", "Space Operations"]:
        if frappe.db.exists("Workspace", ws):
            frappe.delete_doc("Workspace", ws, ignore_permissions=True, force=True)
            print(f"Deleted old workspace: {ws}")

    # Force delete the current AeroSpaceOS so it can be cleanly rebuilt from the JSON
    if frappe.db.exists("Workspace", "AeroSpaceOS"):
        frappe.delete_doc("Workspace", "AeroSpaceOS", ignore_permissions=True, force=True)
        print("Deleted existing AeroSpaceOS workspace for clean rebuild.")

    frappe.db.commit()
    print("Database cleanup complete.")
