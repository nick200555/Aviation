# Copyright (c) 2024, Aviation Team and contributors
import frappe

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "NCR ID", "fieldname": "name", "fieldtype": "Link",
         "options": "Aerospace Quality NCR", "width": 120},
        {"label": "Work Order", "fieldname": "originating_work_order", "fieldtype": "Link",
         "options": "Maintenance Work Order", "width": 140},
        {"label": "Part Number", "fieldname": "part_number", "fieldtype": "Link",
         "options": "Part Number", "width": 130},
        {"label": "Serial Number", "fieldname": "serial_number", "fieldtype": "Data", "width": 110},
        {"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 90},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Disposition", "fieldname": "disposition", "fieldtype": "Data", "width": 110},
        {"label": "CAPA Required", "fieldname": "corrective_and_preventive_action_required",
         "fieldtype": "Check", "width": 100},
        {"label": "CAPA Due", "fieldname": "capa_due_date", "fieldtype": "Date", "width": 110},
        {"label": "Quality Manager", "fieldname": "quality_manager_signature", "fieldtype": "Data", "width": 130},
        {"label": "AS9100 Clause", "fieldname": "as9100_clause_reference", "fieldtype": "Data", "width": 110},
    ]

    conditions = "docstatus < 2"
    if filters.get("severity"):
        conditions += " AND severity = %(severity)s"
    if filters.get("status"):
        conditions += " AND status = %(status)s"

    data = frappe.db.sql(f"""
        SELECT name, originating_work_order, part_number, serial_number, severity, status,
               disposition, corrective_and_preventive_action_required, capa_due_date,
               quality_manager_signature, as9100_clause_reference
        FROM `tabAerospace Quality NCR`
        WHERE {conditions}
        ORDER BY FIELD(severity, 'Critical', 'Major', 'Minor'), creation DESC
    """, filters, as_dict=True)

    return columns, data
