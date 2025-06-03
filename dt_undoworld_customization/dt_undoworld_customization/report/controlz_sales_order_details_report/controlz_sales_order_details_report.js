// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["ControlZ Sales Order Details Report"] = {
	  "filters": [
    {
      "fieldname": "sales_order",
      "label": "Sales Order",
      "fieldtype": "Link",
      "options": "Sales Order"
    },
    {
      "fieldname": "item_code",
      "label": "Item Code",
      "fieldtype": "Link",
      "options": "Item"
    },
    {
      "fieldname": "custom_justpay_id",
      "label": "Juspay Order ID",
      "fieldtype": "Data"
    }
  ]
};
