// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["ControlZ BOM Report"] = {
	"filters": [
    {
        "fieldname": "bom",
        "label": "BOM Number",
        "fieldtype": "Link",
        "options": "BOM"
    },
    {
        "fieldname": "item_code",
        "label": "Item Code",
        "fieldtype": "Link",
        "options": "Item"
    },
    {
        "fieldname": "serial_number",
        "label": "Serial Number",
        "fieldtype": "Link",
        "options": "Serial No"
    },
    {
        "fieldname": "created_by",
        "label": "Created By",
        "fieldtype": "Link",
		"options": "User"
    },
    {
        "fieldname": "from_date",
        "label": "Created From",
        "fieldtype": "Date"
    },
    {
        "fieldname": "to_date",
        "label": "Created To",
        "fieldtype": "Date"
    }
]
};
