// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["ControlZ MES Report"] = {
	"filters": [
 {
            fieldname: "serial_number",
            label: "Serial Number",
            fieldtype: "Link",
			options:"Serial No",
            reqd: 0
        }
	]
};
