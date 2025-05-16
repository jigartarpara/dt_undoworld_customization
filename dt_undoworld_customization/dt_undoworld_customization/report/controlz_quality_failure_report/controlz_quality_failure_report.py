import frappe

def execute(filters=None):
    columns = [
        {"label": "Serial Number", "fieldname": "item_serial_no", "fieldtype": "Link", "options": "Serial No", "width": 180},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Data", "width": 250},
        {"label": "Remark", "fieldname": "remarks", "fieldtype": "Data", "width": 300},
        {"label": "Quality Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": "Date", "fieldname": "report_date", "fieldtype": "Date", "width": 150},
        {"label": "Inspected By", "fieldname": "inspected_by", "fieldtype": "Data", "width": 150},
        {"label": "Verified By", "fieldname": "verified_by", "fieldtype": "Data", "width": 150},
    ]

    filters = filters or {}

    # Build filters for the Quality Inspection doctype
    inspection_filters = {}
    if filters.get("serial_number"):
        inspection_filters["item_serial_no"] = filters["serial_number"]
    if filters.get("item_code"):
        inspection_filters["item_code"] =filters['item_code']
    if filters.get("quality_status"):
        inspection_filters["status"] = filters["quality_status"]
    if filters.get("from_date") and filters.get("to_date"):
        inspection_filters["report_date"] = ["between", [filters["from_date"], filters["to_date"]]]
    if filters.get("inspected_by"):
        inspection_filters["inspected_by"] =filters['inspected_by']
    if filters.get("verified_by"):
        inspection_filters["verified_by"] =filters['verified_by']        

    # Fetch records from Quality Inspection doctype
    inspections = frappe.get_all("Quality Inspection",
        filters=inspection_filters,
        fields=["item_serial_no", "item_code", "remarks", "status", "report_date", "inspected_by", "verified_by"]
    )

    return columns, inspections
