// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["ControlZ Warranty Data Report"] = {
	"filters": [
    {"fieldname": "name", "label": "Serial Number", "fieldtype": "Link", "options": "Serial No"},
    {"fieldname": "model_name", "label": "Model Name", "fieldtype": "Data"},
    {"fieldname": "warranty_start_date", "label": "Warrenty Start Date", "fieldtype": "Date"},
    {"fieldname": "warranty_expiry_date", "label": "Warrenty Expiry Date", "fieldtype": "Date"},
    {"fieldname": "warranty_days", "label": "Warrenty Days", "fieldtype": "Int"},
    {"fieldname": "warranty_status", "label": "Warrenty Status", "fieldtype": "Select", "options": "Active\nExpired"},
    {"fieldname": "imei1", "label": "IMEI1", "fieldtype": "Data"},
    {"fieldname": "imei2", "label": "IMEI2", "fieldtype": "Data"}
]
};
