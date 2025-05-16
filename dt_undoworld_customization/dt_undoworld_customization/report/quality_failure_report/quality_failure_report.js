// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["Quality Failure report"] = {
	 "filters": [
        {
            "fieldname": "serial_number",
            "label": "Serial Number",
            "fieldtype": "Link",
            "options": "Serial No"
        },
        {
            "fieldname": "item_name",
            "label": "Item Name",
            "fieldtype": "Data"
        },
        {
            "fieldname": "quality_status",
            "label": "Quality Status",
            "fieldtype": "Select",
            "options": "\nAccepted\nRejected"  // Adjust options based on your actual statuses
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "inspected_by",
            "label": "Inspected By",
            "fieldtype": "Link",
             "options": "User"
        },
        {
            "fieldname": "verified_by",
            "label": "Verified By",
            "fieldtype": "Data"
        }
    ]
};
