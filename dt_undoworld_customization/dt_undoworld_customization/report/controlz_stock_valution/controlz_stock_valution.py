import frappe
from frappe.utils import getdate, today

def execute(filters=None):
    columns = [
        {"label": "Serial Number", "fieldname": "serial_number", "fieldtype": "Link", "options": "Serial No", "width": 200},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Data", "width": 300},
        {"label": "Location", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 300},
        {"label": "Valuation", "fieldname": "valuation", "fieldtype": "Currency", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
    ]

    data = []

    # Step 1: Get all active serial numbers
    serial_filters = {}

    if filters:
        if filters.get("serial_number"):
            serial_filters["name"] = filters["serial_number"]
        if filters.get("item_code"):
            serial_filters["item_code"] = filters['item_code']
        if filters.get("warehouse"):
            serial_filters["warehouse"] = filters["warehouse"]
            
    serial_nos = frappe.get_all("Serial No",
        filters=serial_filters,
        fields=["name", "item_code", "warehouse", "status"]
    )

    if not serial_nos:
        return columns, []

    serial_no_list = [sn["name"] for sn in serial_nos]

# Step 2: Get latest valuation per serial number from Stock Ledger
    sle_map = {}

    sle_entries = frappe.get_all(
        "Stock Ledger Entry",
        filters={"is_cancelled": 0},
        fields=["serial_no", "serial_and_batch_bundle", "valuation_rate", "posting_date", "posting_time"],
        order_by="posting_date desc, posting_time desc"
    )

    for sle in sle_entries:
        serials = []

        # Case 1: direct serial_no field (multi-line string)
        if sle.serial_no:
            serials = [s.strip() for s in sle.serial_no.split("\n") if s.strip()]

        # Case 2: serial_and_batch_bundle field
        elif sle.serial_and_batch_bundle:
            bundle = frappe.get_doc("Serial and Batch Bundle", sle.serial_and_batch_bundle)
            serials = [s.serial_no for s in bundle.entries if s.serial_no]

        for serial in serials:
            if serial in serial_no_list and serial not in sle_map:
                sle_map[serial] = sle["valuation_rate"]


        # Step 3: Build final data
        for sn in serial_nos:
            data.append({
                "serial_number": sn["name"],
                "item_code": sn["item_code"],
                "warehouse": sn["warehouse"],
                "valuation": sle_map.get(sn["name"], 0.0),
                "status": sn["status"]
            })

        return columns, data
