import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data

def get_columns():
    return [
        {"label": "Serial No", "fieldname": "serial_no", "fieldtype": "Link", "options": "Serial No", "width": 250},
        {"label": "Creation Date", "fieldname": "creation_date", "fieldtype": "Date", "width": 150},
        {"label": "Vendor Name", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 250},
        {"label": "Purchase Order", "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order", "width": 180}
    ]

def get_data():
    # Get all serials
    serials = frappe.get_all("Serial No", fields=["name", "creation"])
    serial_map = {s.name: s.creation.date() for s in serials}
    serial_names = list(serial_map.keys())

    if not serial_names:
        return []

    # Step 1: Find all bundles where serials appear
    bundle_rows = frappe.db.sql("""
        SELECT
            parent AS bundle,
            serial_no
        FROM
            `tabSerial and Batch Entry`
        WHERE
            serial_no IN %(serials)s
    """, {"serials": serial_names}, as_dict=True)

    # Map: serial_no -> list of bundle names
    serial_to_bundles = {}
    for row in bundle_rows:
        serial_to_bundles.setdefault(row.serial_no, []).append(row.bundle)

    if not serial_to_bundles:
        return [{"serial_no": sn, "creation_date": serial_map[sn], "supplier": "", "purchase_order": ""} for sn in serial_names]

    # Step 2: Get all relevant Purchase Receipts and Items
    bundle_list = list({b for bundles in serial_to_bundles.values() for b in bundles})

    purchase_data = frappe.db.sql("""
        SELECT
            pri.serial_and_batch_bundle,
            pri.purchase_order,
            pr.supplier,
            pr.creation
        FROM
            `tabPurchase Receipt Item` pri
        JOIN
            `tabPurchase Receipt` pr ON pr.name = pri.parent
        WHERE
            pri.serial_and_batch_bundle IN %(bundles)s
        ORDER BY
            pr.creation ASC
    """, {"bundles": bundle_list}, as_dict=True)

    # Map: bundle -> first matching purchase record
    bundle_to_purchase = {}
    for row in purchase_data:
        if row.serial_and_batch_bundle not in bundle_to_purchase:
            bundle_to_purchase[row.serial_and_batch_bundle] = {
                "supplier": row.supplier,
                "purchase_order": row.purchase_order
            }

    # Final result
    result = []
    for sn in serial_names:
        creation_date = serial_map[sn]
        bundles = serial_to_bundles.get(sn, [])

        purchase_info = None
        for b in bundles:
            if b in bundle_to_purchase:
                purchase_info = bundle_to_purchase[b]
                break

        result.append({
            "serial_no": sn,
            "creation_date": creation_date,
            "supplier": purchase_info["supplier"] if purchase_info else "",
            "purchase_order": purchase_info["purchase_order"] if purchase_info else ""
        })

    return result
