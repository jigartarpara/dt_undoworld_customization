import frappe
from frappe.model.mapper import get_mapped_doc

def on_update(doc, method):
    if (doc.voucher_type == 'Stock Entry') and (doc.voucher_subtype == 'Manufacture'):
        if doc.is_cancelled != 1:
            if doc.debit > doc.credit:
                bifurcate_gl_for_stock_entry(doc)
            

def bifurcate_gl_for_stock_entry(doc):
    stock_entry_item_list = frappe.get_all('Stock Entry Detail',
                                           filters = {
                                               'parent': doc.voucher_no,
                                               'is_finished_item': 1
                                           },
                                           pluck = 'item_code')
    
    
    