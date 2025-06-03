// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["ControlZ Stock Valution"] = {
	    "filters": [
        {
            "fieldname": "serial_number",
            "label": "Serial Number",
            "fieldtype": "Link",
            "options": "Serial No"
        },
        {
            "fieldname": "item_code",
            "label": "Item Code",
            "fieldtype": "Link",
			 "options": "Item"
        },
        {
            "fieldname": "warehouse",
            "label": "Location",
            "fieldtype": "Link",
            "options": "Warehouse"
        }
    ]
};
