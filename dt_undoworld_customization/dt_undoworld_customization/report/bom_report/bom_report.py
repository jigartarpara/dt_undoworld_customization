import frappe

def execute(filters=None):
    columns = [
        {"label": "BOM Number", "fieldname": "bom", "fieldtype": "Link", "options": "BOM", "width": 300},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 350},
        {"label": "Serial Number", "fieldname": "serial_number", "fieldtype": "Link", "options": "Serial No", "width": 180},
        {"label": "Created Date", "fieldname": "created_date", "fieldtype": "Datetime", "width": 180},
        {"label": "Created By", "fieldname": "created_by", "fieldtype": "Link", "options": "User","width": 200},
    ]

    data = []
    filters = filters or {}

    # Step 1: Filter serial numbers if needed
    serial_nos = []
    if filters.get("serial_number"):
        serial_nos = [filters["serial_number"]]
    else:
        serial_nos = frappe.get_all("Serial No", pluck="name")

    if not serial_nos:
        return columns, []

    # Step 2: Build filters for BOM Item
    bom_item_filters = {
        "custom_serial_no": ["in", serial_nos]
    }
    if filters.get("item_name"):
        bom_item_filters["item_name"] = ["like", f"%{filters['item_name']}%"]
    if filters.get("bom"):
        bom_item_filters["parent"] = filters["bom"]

    # Step 3: Fetch BOM Items
    bom_items = frappe.get_all("BOM Item",
        filters=bom_item_filters,
        fields=["parent", "item_name", "custom_serial_no"]
    )

    if not bom_items:
        return columns, []

    # Step 4: Get BOM metadata
    bom_names = list({item["parent"] for item in bom_items})
    bom_filters = {"name": ["in", bom_names]}

    if filters.get("created_by"):
        bom_filters["owner"] = filters["created_by"]
    if filters.get("from_date") and filters.get("to_date"):
        bom_filters["creation"] = ["between", [filters["from_date"], filters["to_date"]]]

    boms_meta = frappe.get_all("BOM",
        filters=bom_filters,
        fields=["name", "creation", "owner"]
    )

    bom_lookup = {bom["name"]: bom for bom in boms_meta}

    # Step 5: Final data
    for item in bom_items:
        bom = bom_lookup.get(item["parent"])
        if not bom:
            continue

        data.append({
            "bom": bom["name"],
            "item_name": item["item_name"],
            "serial_number": item["custom_serial_no"],
            "created_date": bom["creation"],
            "created_by": bom["owner"],
        })

    return columns, data
