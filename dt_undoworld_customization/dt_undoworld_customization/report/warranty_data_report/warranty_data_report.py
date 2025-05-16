import frappe
from frappe.utils import today, getdate

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        {"label": "Serial Number", "fieldname": "name", "fieldtype": "Link", "options": "Serial No", "width": 180},
        {"label": "Model Name", "fieldname": "model_name", "fieldtype": "Data", "width": 250},
        {"label": "Warrenty Start date", "fieldname": "warranty_start_date", "fieldtype": "Date", "width": 180},
        {"label": "Warrenty Expire date", "fieldname": "warranty_expiry_date", "fieldtype": "Date", "width": 180},
        {"label": "Warrenty Days", "fieldname": "warranty_days", "fieldtype": "Int", "width": 180},
        {"label": "Warrenty Status", "fieldname": "warranty_status", "fieldtype": "Data", "width": 180},
        {"label": "IMEI1", "fieldname": "imei1", "fieldtype": "Data", "width": 200},
        {"label": "IMEI2", "fieldname": "imei2", "fieldtype": "Data", "width": 200},
    ]

    # Build dict-based filters
    filter_dict = {}
    if filters.get("name"):
        filter_dict["name"] = filters["name"]
    if filters.get("model_name"):
        filter_dict["custom_model_name"] = ["like", f"%{filters['model_name']}%"]
    if filters.get("warranty_start_date"):
        filter_dict["custom_warranty_start_date"] = [">=", filters["warranty_start_date"]]
    if filters.get("warranty_expiry_date"):
        filter_dict["warranty_expiry_date"] = ["<=", filters["warranty_expiry_date"]]
    if filters.get("warranty_days"):
        filter_dict["warranty_period"] = filters["warranty_days"]
    if filters.get("imei1"):
        filter_dict["custom_imei1"] = ["like", f"%{filters['imei1']}%"]
    if filters.get("imei2"):
        filter_dict["custom_imei2"] = ["like", f"%{filters['imei2']}%"]

    serial_nos = frappe.get_all("Serial No", filters=filter_dict, fields=[
        "name", "custom_model_name", "custom_warranty_start_date", "warranty_expiry_date", 
        "warranty_period", "custom_imei1", "custom_imei2"
    ])

    data = []
    for sn in serial_nos:
        start_date = sn.custom_warranty_start_date
        expiry_date = sn.warranty_expiry_date
        status = "Expired" if expiry_date and getdate(expiry_date) < getdate(today()) else "Active"

        # Optional additional filter for calculated warranty_status
        if filters.get("warranty_status") and filters["warranty_status"] != status:
            continue

        data.append({
            "name": sn.name,
            "model_name": sn.custom_model_name,
            "warranty_start_date": start_date,
            "warranty_expiry_date": expiry_date,
            "warranty_days": sn.warranty_period,
            "warranty_status": status,
            "imei1": sn.custom_imei1,
            "imei2": sn.custom_imei2,
        })

    return columns, data
