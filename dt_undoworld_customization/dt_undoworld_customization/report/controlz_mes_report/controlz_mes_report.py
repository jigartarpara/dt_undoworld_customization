import frappe
from frappe.utils import get_datetime

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Serial Number", "fieldname": "serial_number", "fieldtype": "Link","options":"Serial No", "width": 150},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
        {"label": "Movement", "fieldname": "movement", "fieldtype": "Data", "width": 120},
        {"label": "Movement Date And Time", "fieldname": "movement_datetime", "fieldtype": "Datetime", "width": 180},
        {"label": "Final Status", "fieldname": "final_status", "fieldtype": "Data", "width": 120},
        {"label": "Work Order Status", "fieldname": "work_order_status", "fieldtype": "Data", "width": 150},
    ]

    # Step 1: Apply serial number filter
    conditions = ""
    params = []

    if filters.get("serial_number"):
        conditions += "AND sn.name = %s"
        params.append(filters["serial_number"])

    # Step 2: Fetch all relevant Serial No in one go
    serials = frappe.db.sql(f"""
        SELECT sn.name, sn.item_name, sn.status, sn.work_order
        FROM `tabSerial No` sn
        WHERE 1=1 {conditions}
    """, tuple(params), as_dict=True)

    serial_names = [s.name for s in serials]

    if not serial_names:
        return columns, []

    # Step 3: Fetch latest movement entries in one query
    sle_map = {}
    sle_entries = frappe.db.sql(f"""
        SELECT serial_no, posting_date, posting_time, voucher_type
        FROM `tabStock Ledger Entry`
        WHERE serial_no IN (%s)
        ORDER BY posting_date DESC, posting_time DESC
    """ % ','.join(['%s'] * len(serial_names)), tuple(serial_names), as_dict=True)

    for entry in sle_entries:
        for serial in entry.serial_no.split('\n'):  # Handles multiple serials in one SLE
            if serial and serial not in sle_map:
                sle_map[serial] = entry

    # Step 4: Fetch all work order statuses in one query
    work_orders = list(set(s.work_order for s in serials if s.work_order))
    work_order_map = {}

    if work_orders:
        work_order_statuses = frappe.db.get_all(
            "Work Order",
            filters={"name": ["in", work_orders]},
            fields=["name", "status"]
        )
        work_order_map = {wo.name: wo.status for wo in work_order_statuses}

    # Step 5: Prepare data
    data = []

    for s in serials:
        sle = sle_map.get(s.name)
        movement = sle["voucher_type"] if sle else "N/A"
        movement_dt = get_datetime(f"{sle['posting_date']} {sle['posting_time']}") if sle else None
        wo_status = work_order_map.get(s.work_order, "N/A") if s.work_order else "N/A"

        data.append({
            "serial_number": s.name,
            "item_name": s.item_name,
            "movement": movement,
            "movement_datetime": movement_dt,
            "final_status": s.status,
            "work_order_status": wo_status
        })

    return columns, data
