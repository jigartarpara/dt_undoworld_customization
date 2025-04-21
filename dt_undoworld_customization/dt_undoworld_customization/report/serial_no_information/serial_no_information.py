import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data

def get_columns():
    return [
        {"label": "Serial No", "fieldname": "serial_no", "fieldtype": "Link", "options": "Serial No", "width": 250},
        {"label": "Creation Date", "fieldname": "creation_date", "fieldtype": "Date", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 200},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": "IMEI 1", "fieldname": "custom_imei1", "fieldtype": "Data", "width": 180},
        {"label": "Vendor Name", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 250},
        {"label": "Purchase Order", "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order", "width": 180},
        {"label": "Delivered Date", "fieldname": "delivered_date", "fieldtype": "Date", "width": 150},
        {"label": "Consumed Date", "fieldname": "consumed_date", "fieldtype": "Date", "width": 150}
    ]

def get_data():
    serials = frappe.get_all("Serial No", fields=["name", "creation", "status", "warehouse", "item_code", "custom_imei1"])
    if not serials:
        return []

    serial_map = {
        s.name: {
            "creation_date": s.creation.date(),
            "status": s.status,
            "warehouse": s.warehouse,
            "item_code": s.item_code,
            "custom_imei1": s.custom_imei1
        }
        for s in serials
    }
    serial_names = list(serial_map.keys())

    # --- Step 1: Serial to Bundle Map ---
    bundle_rows = frappe.db.sql("""
        SELECT parent AS bundle, serial_no
        FROM `tabSerial and Batch Entry`
        WHERE serial_no IN %(serials)s
    """, {"serials": serial_names}, as_dict=True)

    serial_to_bundles = {}
    bundle_set = set()
    for row in bundle_rows:
        serial_to_bundles.setdefault(row.serial_no, []).append(row.bundle)
        bundle_set.add(row.bundle)

    # --- Step 2: Bundle to First Purchase Receipt ---
    purchase_data = frappe.db.sql("""
        SELECT pri.serial_and_batch_bundle, pri.purchase_order, pr.supplier
        FROM `tabPurchase Receipt Item` pri
        JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
        WHERE pri.serial_and_batch_bundle IN %(bundles)s
        ORDER BY pr.creation ASC
    """, {"bundles": list(bundle_set)}, as_dict=True)

    bundle_to_purchase = {}
    for row in purchase_data:
        if row.serial_and_batch_bundle not in bundle_to_purchase:
            bundle_to_purchase[row.serial_and_batch_bundle] = {
                "supplier": row.supplier,
                "purchase_order": row.purchase_order
            }

    # --- Step 3: Preload Delivery Dates for Delivered Serials ---
    delivered_serials = [s for s in serial_map if serial_map[s]["status"] == "Delivered"]
    delivered_map = {}
    if delivered_serials:
        delivery_rows = frappe.db.sql("""
            SELECT dni.serial_no, dn.posting_date
            FROM `tabDelivery Note Item` dni
            JOIN `tabDelivery Note` dn ON dn.name = dni.parent
            WHERE dni.serial_no IN %(serials)s
            ORDER BY dn.posting_date DESC
        """, {"serials": delivered_serials}, as_dict=True)

        for row in delivery_rows:
            # only keep first occurrence (latest)
            if row.serial_no not in delivered_map:
                delivered_map[row.serial_no] = row.posting_date

    # --- Step 4: Preload Consumed Dates for Consumed Serials ---
    consumed_serials = [s for s in serial_map if serial_map[s]["status"] == "Consumed"]
    consumed_map = {}
    if consumed_serials:
        consumed_rows = frappe.db.sql("""
            SELECT sed.serial_no, se.posting_date
            FROM `tabStock Entry Detail` sed
            JOIN `tabStock Entry` se ON se.name = sed.parent
            WHERE sed.serial_no IN %(serials)s
            ORDER BY se.posting_date DESC
        """, {"serials": consumed_serials}, as_dict=True)

        for row in consumed_rows:
            if row.serial_no not in consumed_map:
                consumed_map[row.serial_no] = row.posting_date

    # --- Step 5: Final Row Build ---
    result = []
    for sn in serial_names:
        info = serial_map[sn]
        bundles = serial_to_bundles.get(sn, [])
        purchase_info = next((bundle_to_purchase.get(b) for b in bundles if bundle_to_purchase.get(b)), None)

        result.append({
            "serial_no": sn,
            "creation_date": info["creation_date"],
            "status": info["status"],
            "warehouse": info["warehouse"],
            "item_code": info["item_code"],
            "custom_imei1": info["custom_imei1"],
            "supplier": purchase_info["supplier"] if purchase_info else "",
            "purchase_order": purchase_info["purchase_order"] if purchase_info else "",
            "delivered_date": delivered_map.get(sn),
            "consumed_date": consumed_map.get(sn)
        })

    return result
