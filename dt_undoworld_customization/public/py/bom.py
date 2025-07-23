import frappe

def before_validate(doc, method):
    # print('\n\n\n\n')
    if len(doc.scrap_items)> 0:
        return 1
    flag = 0 
    for d in doc.items:
        if d.custom_serial_no == '':
            d.custom_serial_no = None
        if d.custom_serial_no != None:
            flag =1
            # print ('found')
            break
    if flag == 1:
        # print ('inside loop')
        sum = 0
        for d in doc.items:
            if d.custom_serial_no == None:
                sum += d.amount
        if sum > 0:
            pass
            # doc.append('scrap_items', {
            #     'item_code': frappe.db.get_single_value('DT-Customization Settings', 'scrap_item'),
            #     'qty': 1,
            #     'rate': sum
            # })
    # frappe.throw('test code')

def validate(doc,method):
    # frappe.throw('fdsa')
    rm_total = 0
    phone_value_rate = 0
    phone_item = ''
    for d in doc.items:
        if d.custom_serial_no == '':
            d.custom_serial_no = None
        if d.custom_serial_no != None:
            phone_value_rate = frappe.get_value('Serial and Batch Entry',
                                              {
                                                  'serial_no': d.custom_serial_no,
                                                  'docstatus': 1
                                              }, 'incoming_rate')
            phone_item = d.item_code
            d.base_rate = d.rate = phone_value_rate
            d.base_amount = d.amount = phone_value_rate * d.qty
            
        rm_total += d.base_amount
    if (phone_value_rate > 0) and (phone_item != ''):
        for d in doc.exploded_items:
            if d.item_code == phone_item:
                d.rate = phone_value_rate
                d.amount = phone_value_rate * d.qty_consumed_per_unit
            
    doc.raw_material_cost = rm_total
    doc.total_cost = rm_total - doc.scrap_material_cost