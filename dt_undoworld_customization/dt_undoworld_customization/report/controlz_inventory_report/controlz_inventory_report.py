import frappe
from frappe.utils import flt

def execute(filters=None):
    # -----------------------------------------------------------------------
    # 1. Column definitions
    # -----------------------------------------------------------------------
    columns = [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 160},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 220},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 110},
        {"label": "Location", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 200},
        {"label": "Valuation", "fieldname": "valuation", "fieldtype": "Currency", "width": 140},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]

    # -----------------------------------------------------------------------
    # 2. Filter processing
    # -----------------------------------------------------------------------
    bin_filters = {}
    if filters:
        if filters.get("item_code"):
            bin_filters["item_code"] = filters["item_code"]
        if filters.get("location"):
            bin_filters["warehouse"] = filters["location"]

    # -----------------------------------------------------------------------
    # 3. Fetch stock data from Bin table
    # -----------------------------------------------------------------------
    bins = frappe.get_all(
        "Bin",
        filters=bin_filters,
        fields=["item_code", "warehouse", "actual_qty", "valuation_rate"]
    )

    if not bins:
        return columns, []

    # -----------------------------------------------------------------------
    # 4. Get item names and statuses
    # -----------------------------------------------------------------------
    item_codes = list({b.item_code for b in bins})
    items = frappe.get_all(
        "Item",
        filters={"name": ["in", item_codes]},
        fields=["name", "item_name", "disabled"]
    )
    item_map = {it.name: it for it in items}

    # -----------------------------------------------------------------------
    # 5. Assemble data rows
    # -----------------------------------------------------------------------
    data = []
    for b in bins:
        item = item_map.get(b.item_code)
        if not item:
            continue

        data.append({
            "item_code": b.item_code,
            "item_name": item.item_name,
            "qty": flt(b.actual_qty, 3),
            "warehouse": b.warehouse,
            "valuation": flt(b.actual_qty) * flt(b.valuation_rate or 0),
            "status": "Active" if not item.disabled else "Disabled",
        })

    return columns, data
