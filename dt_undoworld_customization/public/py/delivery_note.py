import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.delivery_note.delivery_note import *

def on_submit(doc, method):
    if doc.is_return == 1:
        return_consumable_scrap(doc)
    # frappe.throw('coding going on...')
        

def return_consumable_scrap(doc):
    se_doc_name =  frappe.db.exists('Stock Entry',
                        {'docstatus': 1,
                         'custom_delivery_note': doc.return_against})
    if se_doc_name:
        new_doc = get_mapped_doc(
            'Stock Entry',
            se_doc_name,
            {
                'Stock Entry':{
                    'doctype': 'Stock Entry',
                    'field_map': {'stock_entry_type': 'stock_entry_type'},
                },
                'Stock Entry Detail':{
                    'doctype': 'Stock Entry Detail',
                    'field_map': {
                        'item_code': 'item_code',
                        'qty': 'qty',
                        'use_serial_batch_fields': 'use_serial_batch_fields',
                        'serial_no': 'serial_no',
                        't_warehouse': 's_warehouse' 
                    }          
                }
            },
            ignore_permissions=True
        )
        
        # print ('\n\n\n\n\n')
        new_doc.stock_entry_type = 'Material Receipt'
        
        for d in new_doc.items:
            d.t_warehouse = d.s_warehouse
            d.s_warehouse = None
            print (d.serial_no)
            
        new_doc.save()
        new_doc.custom_delivery_note = doc.name
        new_doc.submit()
        # frappe.db.commit()
        # print (new_doc)
