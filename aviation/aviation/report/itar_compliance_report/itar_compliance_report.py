# Copyright (c) 2024, Aviation Team and contributors
import frappe
from frappe.utils import getdate, nowdate, add_days

def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Record ID", "fieldname": "name", "fieldtype": "Link",
         "options": "ITAR EAR Access Control", "width": 120},
        {"label": "Reference DocType", "fieldname": "ref_doctype", "fieldtype": "Data", "width": 140},
        {"label": "Reference Document", "fieldname": "ref_docname", "fieldtype": "Data", "width": 160},
        {"label": "Jurisdiction", "fieldname": "jurisdiction", "fieldtype": "Data", "width": 100},
        {"label": "USML Category", "fieldname": "usml_category", "fieldtype": "Data", "width": 120},
        {"label": "ECCN Number", "fieldname": "eccn_number", "fieldtype": "Data", "width": 110},
        {"label": "License Required", "fieldname": "export_license_required", "fieldtype": "Check", "width": 110},
        {"label": "License ID", "fieldname": "export_license_id", "fieldtype": "Data", "width": 120},
        {"label": "License Expiry", "fieldname": "export_license_expiry", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "license_status", "fieldtype": "Data", "width": 110},
        {"label": "Next Review", "fieldname": "next_review_date", "fieldtype": "Date", "width": 120},
    ]

    data_raw = frappe.db.sql("""
        SELECT name, ref_doctype, ref_docname, jurisdiction, usml_category, eccn_number,
               export_license_required, export_license_id, export_license_expiry, next_review_date
        FROM `tabITAR EAR Access Control`
        ORDER BY jurisdiction, ref_doctype
    """, as_dict=True)

    today = getdate(nowdate())
    data = []
    for row in data_raw:
        if row.get("export_license_expiry"):
            expiry = getdate(row["export_license_expiry"])
            if expiry < today:
                row["license_status"] = "EXPIRED"
            elif expiry <= getdate(add_days(nowdate(), 30)):
                row["license_status"] = "Expiring Soon"
            else:
                row["license_status"] = "Valid"
        else:
            row["license_status"] = "N/A"
        data.append(row)

    return columns, data
