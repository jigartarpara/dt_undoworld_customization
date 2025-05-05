// Copyright (c) 2025, DTPL and contributors
// For license information, please see license.txt

frappe.query_reports["Serial Number Information"] = {
	"filters": [
        {
            fieldname: "serial_no",
            label: "Serial No",
            fieldtype: "Link",
            options: "Serial No"
        },
        {
            fieldname: "creation_date",
            label: "Creation Date",
            fieldtype: "Date"
        },
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "\nActive\nInactive\nDelivered\nConsumed\nExpired"
        },
        {
            fieldname: "warehouse",
            label: "Warehouse",
            fieldtype: "Link",
            options: "Warehouse"
        },
        {
            fieldname: "item_code",
            label: "Item Code",
            fieldtype: "Link",
            options: "Item"
        },
        {
            fieldname: "custom_imei1",
            label: "IMEI 1",
            fieldtype: "Data"
        },
        {
            fieldname: "supplier",
            label: "Vendor Name",
            fieldtype: "Link",
            options: "Supplier"
        },
        {
            fieldname: "purchase_order",
            label: "Purchase Order",
            fieldtype: "Link",
            options: "Purchase Order"
        },
        {
            fieldname: "delivered_date",
            label: "Delivered Date",
            fieldtype: "Date"
        },
        {
            fieldname: "consumed_date",
            label: "Consumed Date",
            fieldtype: "Date"
        }
    ]
};
