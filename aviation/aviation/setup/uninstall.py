import frappe

def before_uninstall():
    """Cleanup before app uninstallation."""
    # Note: DocTypes are automatically removed by Frappe on uninstall.
    # Add any custom field cleanup or data archival here if needed.
    frappe.msgprint("Aviation Management System is being uninstalled. All aviation DocTypes and data will be removed.")
