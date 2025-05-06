import frappe

def before_submit(doc, method):
    # frappe.throw('testing')
    print ('\n\n\n\n\n')
    # if doc.is_return == 1:
    #     clear_warranty_dates(doc.items)
        

def clear_warranty_dates(items):
    # frappe.throw('in function')
    for item in items:
        if item.delivery_note:
            s_b_bundle = frappe.db.get_value('Delivery Note Item', item.dn_detail, 'serial_and_batch_bundle')
            serial_list = frappe.db.get_all('Serial and Batch Entry',
                                            filters = {
                                                'parent': s_b_bundle
                                            },
                                            pluck = 'serial_no')
            for serial in serial_list:
                # frappe.db.set_value('Serial No', 'custom_warranty_start_date', None)
                # frappe.db.set_value('Serial No', 'warranty_expiry_date', None)
                frappe.db.set_value('Serial No', serial, {
                                        'custom_warranty_start_date': None,
                                        'warranty_expiry_date': None
                                    })
                