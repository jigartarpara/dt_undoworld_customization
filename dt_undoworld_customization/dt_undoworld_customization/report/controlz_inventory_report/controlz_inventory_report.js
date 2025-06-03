// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["ControlZ Inventory Report"] = {
	 "filters": [
    {
      "fieldname": "item_code",
      "label": "Item Code",
      "fieldtype": "Link",
      "options": "Item",
      "default": "",
      "reqd": 0
    },
    {
      "fieldname": "location",
      "label": "Location",
      "fieldtype": "Link",
      "options": "Warehouse",
      "default": "",
      "reqd": 0
    }
  ]
};
