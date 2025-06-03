import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 140},
        {"label": "Date", "fieldname": "transaction_date", "fieldtype": "Date", "width": 110},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 180},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Juspay Order ID", "fieldname": "custom_justpay_id", "fieldtype": "Data", "width": 180},
        {"label": "Customer State", "fieldname": "state", "fieldtype": "Data", "width": 150},
        {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 250},
        {"label": "Email ID", "fieldname": "email", "fieldtype": "Data", "width": 180},
        {"label": "Mobile Number", "fieldname": "mobile", "fieldtype": "Data", "width": 140},
    ]

    conditions = ""
    values = {}

    if filters:
        if filters.get("sales_order"):
            conditions += " AND so.name = %(sales_order)s"
            values["sales_order"] = filters["sales_order"]
        if filters.get("item_code"):
            conditions += " AND soi.item_code = %(item_code)s"
            values["item_code"] = filters["item_code"]
        if filters.get("custom_justpay_id"):
            conditions += " AND so.custom_justpay_id = %(custom_justpay_id)s"
            values["custom_justpay_id"] = filters["custom_justpay_id"]
        if filters.get("from_date"):
            conditions += " AND so.transaction_date >= %(from_date)s"
            values["from_date"] = filters["from_date"]
        if filters.get("to_date"):
            conditions += " AND so.transaction_date <= %(to_date)s"
            values["to_date"] = filters["to_date"]

    query = f"""
        SELECT
            soi.parent AS sales_order,
            so.transaction_date,
            soi.item_code,
            soi.qty,
            soi.amount,
            so.custom_justpay_id,
            addr.state,
            addr.address_line1,
            so.custom_email_id,
            so.custom_mobile_number
        FROM (
            SELECT soi.*,
                   ROW_NUMBER() OVER (PARTITION BY soi.parent ORDER BY soi.idx ASC) as row_num
            FROM `tabSales Order Item` soi
        ) soi
        JOIN `tabSales Order` so ON so.name = soi.parent
        LEFT JOIN `tabAddress` addr ON so.customer_address = addr.name
        WHERE soi.row_num = 1 AND so.docstatus < 2 {conditions}
        ORDER BY soi.parent DESC
    """

    results = frappe.db.sql(query, values, as_dict=True)

    data = []
    for row in results:
        data.append({
            "sales_order": row.sales_order,
            "transaction_date": row.transaction_date,
            "item_code": row.item_code,
            "qty": row.qty,
            "amount": flt(row.amount),
            "custom_justpay_id": row.custom_justpay_id,
            "state": row.state or "",
            "address": row.address_line1 or "",
            "email": row.custom_email_id or "",
            "mobile": row.custom_mobile_number or ""
        })

    return columns, data
