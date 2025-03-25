# Copyright (c) 2024, DTPL and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document


class PhonecheckLog(Document):
    def on_submit(self):
        update_to_serial_no(self.items)
        


def update_to_serial_no(items):
    for d in items:
        if d.itemsku_serial_no == '':
            d.itemsku_serial_no = None
        if d.itemsku_serial_no == None:
            continue
        serial_no = d.itemsku_serial_no
        if frappe.db.exists("Serial No", {"name": serial_no}):
            frappe.db.set_value('Serial No', serial_no, {
                'custom_model_name': d.model_name,
                'custom_model_no': d.model_no,
                'custom_imei1': d.imei,
                'custom_imei2': d.imei2,
                'custom_eid': d.udid,
                'custom_sn': d.serial,
                'custom_ram': d.ram or '',
                'custom_rom': d.memory,
                'custom_quality_check': d.quality_test,
                'custom_remarks': d.remarks
                })
