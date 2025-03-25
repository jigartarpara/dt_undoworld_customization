import frappe

def on_submit(doc, method):
    if (doc.voucher_type == 'Delivery Note') and (doc.type_of_transaction == 'Outward'):
        consume_scrap_material(doc)
    if doc.voucher_type == "Stock Entry":
        set_device_detail_to_serial_no(doc)

    # frappe.throw('halt')

def consume_scrap_material(doc):
    # print ('\n\n\n\n')
    if frappe.db.get_value('Delivery Note', doc.voucher_no, 'docstatus') == 1:
        for serial_item in doc.entries:
            if (serial_item.serial_no[-2:] == '-1'):
                scrap_serial = serial_item.serial_no[:-2] + '-C'
                if frappe.db.exists('Serial No', scrap_serial):
                    # print (frappe.db.get_value('Serial No', scrap_serial, 'warehouse'))
                    se_doc = frappe.new_doc('Stock Entry')
                    se_doc.stock_entry_type = 'Material Issue'
                    item = {
                        'item_code': frappe.db.get_value('Serial No', scrap_serial, 'item_code'),
                        'qty': 1,
                        'uom': frappe.db.get_value('Item',(frappe.db.get_value('Serial No', scrap_serial, 'item_code')), 'stock_uom'),
                        # 'stock_uom': 'Pcs',
                        # 'conversion_factor': 1,
                        's_warehouse': (frappe.db.get_value('Serial No', scrap_serial, 'warehouse')),
                        'use_serial_batch_fields': 1,
                        'serial_no': scrap_serial
                    }
                    se_doc.append('items', item)
                    se_doc.custom_delivery_note = doc.voucher_no
                    se_doc.save()
                    # frappe.db.commit()
                    se_doc.submit()


def set_device_detail_to_serial_no(doc):
    if doc.type_of_transaction == 'Inward':
        for d in doc.entries:
            # frappe.throw(d.serial_no)
            if d.serial_no[-2:] == '-1':
                # serial_no_doc = frappe.get_doc('Serial No', d.serial_no)
                old_serial_no = d.serial_no[:-2]
                custom_model_name,custom_model_no,custom_imei1,custom_imei2,custom_eid, custom_sn,custom_ram,custom_rom = frappe.db.get_value('Serial No', old_serial_no, 
                                                                                                                                               ['custom_model_name',
                                                                                                                                                 'custom_model_no',
                                                                                                                                                 'custom_imei1',
                                                                                                                                                 'custom_imei2',
                                                                                                                                                 'custom_eid', 
                                                                                                                                                 'custom_sn',
                                                                                                                                                 'custom_ram',
                                                                                                                                                 'custom_rom'])
                frappe.db.set_value('Serial No', d.serial_no, {
                    'custom_model_name': custom_model_name,
                    'custom_model_no': custom_model_no,
                    'custom_imei1': custom_imei1,
                    'custom_imei2':custom_imei2 ,
                    'custom_eid': custom_eid, 
                    'custom_sn': custom_sn,
                    'custom_ram': custom_ram,
                    'custom_rom': custom_rom
                })

                # frappe.throw(serial_no_doc.item_code)
        # frappe.throw('halt')