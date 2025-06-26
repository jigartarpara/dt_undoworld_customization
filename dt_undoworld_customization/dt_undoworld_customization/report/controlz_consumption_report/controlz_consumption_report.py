# File: your_custom_app/your_custom_app/report/consumption_report/consumption_report.py

import frappe
from frappe import _

def execute(filters=None):
    columns = [
        _("Work Order") + ":Link/Work Order:120",
        _("Item Name") + ":Link/Item:150",
        _("Device Serial Number") + ":Data:150",
        _("Spare Part Serial") + ":Data:150",
        _("Device Cost") + ":Currency:120",
        _("Spare Part Cost") + ":Currency:120",
        _("Net Cost") + ":Currency:120",
        _("Avrg Device Cost") + ":Currency:150",
        _("Avrg Spare Part Cost") + ":Currency:150"
    ]

    data = []

    # Example SQL - replace table and field names as per your actual DocTypes
    results = frappe.db.sql("""
       SELECT 
    wo.name AS work_order,
    wo.production_item AS item_name,
    dsn.serial_no AS device_serial_number,
    sps.serial_no AS spare_part_serial,
    dsn.purchase_rate AS device_cost,
    sps.purchase_rate AS spare_part_cost,
    (IFNULL(dsn.purchase_rate, 0) + IFNULL(sps.purchase_rate, 0)) AS net_cost,
    (SELECT AVG(purchase_rate) FROM `tabSerial No` WHERE item_group = 'Device') AS avg_device_cost,
    (SELECT AVG(purchase_rate) FROM `tabSerial No` WHERE item_group = 'Spare Part') AS avg_spare_cost
FROM 
    `tabWork Order` wo
LEFT JOIN `tabSerial No` dsn ON dsn.work_order = wo.name AND dsn.item_group = 'Device'
LEFT JOIN `tabSerial No` sps ON sps.work_order = wo.name AND sps.item_group = 'Spare Part'
WHERE 
    wo.docstatus = 1
    """, as_dict=True)

    for row in results:
        data.append([
            row.work_order,
            row.item_name,
            row.device_serial_number,
            row.spare_part_serial,
            row.device_cost,
            row.spare_part_cost,
            row.net_cost,
            row.avg_device_cost,
            row.avg_spare_cost
        ])

    return columns, data
