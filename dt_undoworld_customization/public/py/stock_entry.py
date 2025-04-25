import frappe
from erpnext.stock.doctype.stock_entry.stock_entry import *


def before_validate(doc, method):
    print ('\n\n\n\n\n\n')
    if  doc.stock_entry_type not in ['Manufacture', 'Material Transfer for Manufacture']:
        return 1
    if doc.bom_no == None:
        return 1
    
    if doc.custom_finished_good_value_changed == 1:
        return 1
    # frappe.throw('testing')
    s_no =  get_serial_no(doc.bom_no)
    spare_parts_serial_nos = fetch_item_wise_serial_nos(doc.work_order)
    old_item_rate = fetch_old_item_rate(doc.items, s_no[0])
    print(s_no[0] )
    if old_item_rate > 0:
        for d  in doc.items:
            if d.item_code == s_no[1]:
                # frappe.throw('inside the if condition')
                d.use_serial_batch_fields = 1
                d.serial_no = s_no[0]
            if (doc.stock_entry_type == 'Manufacture') and (d.item_code in spare_parts_serial_nos):
                d.use_serial_batch_fields = 1
                d.serial_no = spare_parts_serial_nos[d.item_code]
            if d.is_finished_item == 1:
                d.use_serial_batch_fields = 1
                d.serial_no = s_no[0] + '-1'
            if check_consumable_item(d.item_code) == 1:
                d.use_serial_batch_fields = 1
                d.serial_no = s_no[0] + '-C'
                sum_of_consumables = get_totals(doc.items, s_no[1])
                # print(sum_of_consumables)
                d.basic_rate = (sum_of_consumables - old_item_rate)
    
    
    # frappe.throw('code in process')
    

    
def validate(doc,method):
    # return 1
    if doc.custom_finished_good_value_changed != 1:
        old_item_rate = fetch_old_item_rate(doc.items)
        for d in doc.items:
            if d.is_finished_item == 1:
                d.basic_rate = old_item_rate
                d.valuation_rate = old_item_rate
                d.basic_amount = old_item_rate
                d.amount = old_item_rate
        doc.total_incoming_value = doc.total_outgoing_value
        doc.value_difference = 0
    # doc.custom_finished_good_value_changed = 1
    
    
    

def fetch_old_item_rate(items, sno = None):
    """This code store the valuation rate of the old
    phone, so that the vaalue can be copied to the refurbished phone. 
    NOTE: This also assigns the serial no to the old phone in material transfer
    to manuifacture state"""
    for item in items:
        if (frappe.db.get_value('Item', item.item_code, 'is_ineligible_for_itc')) == 1:
            # old_sno =  frappe.get_value('Serial and Batch Entry',
            #                             {'parent': item.serial_and_batch_bundle})
            if sno != None:                 
                item.use_serial_batch_fields = 1
                item.serial_no = sno
            return  item.basic_rate
    return 0


def get_serial_no(bom):
    """This function fetches the serial no of the old phone 
    from the BOM item list which have old_phone check ticked"""
    query = f"""
            SELECT
                custom_serial_no, item_code
            FROM 
                `tabBOM Item`
            WHERE
                parent = '{bom}'
                AND custom_is_old_phone = 1
            LIMIT 1"""
    sno = frappe.db.sql(query)
    return (sno[0])




def testing():
    print ('check')
    # print(get_totals('MAT-STE-2024-00019', 'Apple iPhone 11-PUR-4GB-256GB -old'))
    print(fetch_item_wise_serial_nos('MFG-WO-2024-00011'))



    
def check_consumable_item(item_code):
    if item_code == frappe.db.get_single_value('DT-Customization Settings', 'scrap_item'):
        return 1

def get_totals(items, item_code):
    
    # print (doc_name, item_code)
    sum = 0
    consumable_item = frappe.db.get_single_value('DT-Customization Settings', 'scrap_item')
    for item in items:
        if (item.item_code != item_code) and (item.item_code != consumable_item):
            sum += item.amount

    # print(sum)
    return sum

# def on_submit(doc,method):
#     if (doc.stock_entry_type == 'Material Transfer for Manufacture') and (doc.bom_no != None):
#         create_stock_entry_for_old_parts(doc)


# def create_stock_entry_for_old_parts(doc):
#     # frappe.throw('coding in process')    
#     item_list = frappe.get_all('BOM Item',
#                                filters = {
#                                    'parent': doc.bom_no,
#                                    'custom_is_old_phone': 0,
#                                    'custom_is_part_missing': 0
#                                },
#                                fields = ['item_code', 'stock_qty', 'stock_uom', 'uom', 'conversion_factor', 'qty'])
#     if len(item_list) == 0:
#         return
    
#     stock_entry_item_list = []
#     for d in doc.items:
#         stock_entry_item_list.append(d.item_code)
    
#     new_stock = frappe.new_doc('Stock Entry')
#     new_stock.stock_entry_type = 'Material Receipt'
#     new_stock.to_warehouse = doc.to_warehouse
#     for item in item_list:
#         if item.item_code in stock_entry_item_list:
#             row = {
#                 'item_code': item.item_code,
#                 'qty': item.qty,
#                 'uom': item.uom,
#                 'transfer_qty': item.stock_qty,
#                 't_warehouse':"Old Parts Warehouse - UW",
#                 'conversion_factor': item.conversion_factor,
#                 'allow_zero_valuation_rate': 1,
#                 'valuation_rate': 0,
#                 'basic_rate': 0,
#                 'basic_amount': 0,
#                 'amount': 0
#             }
#             new_stock.append('items', row)
            
#     if len(new_stock.items) > 0:
#         new_stock.save()
#         new_stock.submit()
#         doc.db_set('custom_old_part_stock_entry', new_stock.name)


def fetch_item_wise_serial_nos(work_order, se_type = None):
    other_se_name = frappe.db.exists('Stock Entry',
                                     {
                                         'work_order': work_order,
                                         'stock_entry_type': 'Material Transfer for Manufacture',
                                         'docstatus': 1
                                     })
    if other_se_name:
        s_b_list = frappe.get_all('Stock Entry Detail',
                                  filters = {
                                      'parent': other_se_name,
                                    #   'serial_no': ['=','']
                                  },
                                  fields = ['item_code', 'serial_and_batch_bundle'])
        item_wise_serial_list = {}
        for s_b in s_b_list:
            s_nos = ''
            for s_no in frappe.get_all('Serial and Batch Entry', filters ={'parent': s_b.serial_and_batch_bundle}, pluck = 'serial_no'):
                s_nos += s_no + ', '
            item_wise_serial_list[s_b.item_code] = s_nos
        return item_wise_serial_list
    return 0



@frappe.whitelist()
def se_for_new_fg( old_fg_row, old_se_name = None, new_fg_item_code = None):

    if old_se_name == None:
        return 0
    
    if new_fg_item_code == None:
        return 0
    
    from json import loads
    old_fg_row = frappe._dict(loads(old_fg_row))


    #### SUBMITING THE OTHER STCOK ENTRY TO PROCEED FURTHER ####
    old_se_doc = frappe.get_doc('Stock Entry', old_se_name)
    old_se_doc.submit()
    if old_fg_row.serial_no == None:
        frappe.throw('No serial no set in finished goods')
        return 0
    
    #### CREATING A NEW STOCK ENTRY FOR REPACK ####
    new_stock = frappe.new_doc('Stock Entry')
    new_stock.stock_entry_type = 'Repack'
    
    ### FEED OLD FG ITEM ###
  
    old_fg_item_row = {
        'item_code': old_fg_row.item_code,
        'qty': old_fg_row.qty,
        'uom': old_fg_row.uom,
        'transfer_qty': old_fg_row.transfer_qty,
        'conversion_factor': old_fg_row.conversion_factor,
        's_warehouse': old_fg_row.t_warehouse,
        'use_serial_batch_fields': 1,
        'serial_no': old_fg_row.serial_no
    }
    new_stock.append('items', old_fg_item_row)
    
    new_serial_no = str(old_fg_row.serial_no)[:-2] + '-2'
    
    
    ### FEED NEW FG ITEM ###
    
    
    new_fg_item_row = {
        'item_code': new_fg_item_code,
        'is_finished_item': 1,
        'qty': old_fg_row.qty,
        'uom': old_fg_row.uom,
        'transfer_qty': old_fg_row.transfer_qty,
        'conversion_factor': old_fg_row.conversion_factor,
        't_warehouse': old_fg_row.t_warehouse,
        'use_serial_batch_fields': 1,
        'serial_no': new_serial_no
    }
    new_stock.append('items', new_fg_item_row)
    new_stock.custom_finished_good_value_changed = 1
    
    new_stock.save()
    new_stock.submit()

    old_se_doc.db_set('custom_new_fg_item_stock_entry_link', new_stock.name)
    return 1




def before_cancel(doc, method):
    if doc.stock_entry_type == 'Repack':
        linked_se_doc_name = frappe.db.exists('Stock Entry', 
                                            {
                                                'docstatus': 1,
                                                'custom_new_fg_item_stock_entry_link': doc.name
                                            })
        if linked_se_doc_name:
            frappe.db.set_value('Stock Entry', linked_se_doc_name, 'custom_new_fg_item_stock_entry_link', '')


class customStockEntry(StockEntry): 
      
	@frappe.whitelist()
	def get_items(self):
		self.set("items", [])
		self.validate_work_order()

		if self.purpose == "Disassemble":
			return self.get_items_for_disassembly()

		if not self.posting_date or not self.posting_time:
			frappe.throw(_("Posting date and posting time is mandatory"))

		self.set_work_order_details()
		self.flags.backflush_based_on = frappe.db.get_single_value(
			"Manufacturing Settings", "backflush_raw_materials_based_on"
		)

		if self.bom_no:
			backflush_based_on = frappe.db.get_single_value(
				"Manufacturing Settings", "backflush_raw_materials_based_on"
			)

			if self.purpose in [
				"Material Issue",
				"Material Transfer",
				"Manufacture",
				"Repack",
				"Send to Subcontractor",
				"Material Transfer for Manufacture",
				"Material Consumption for Manufacture",
			]:
				if self.work_order and self.purpose == "Material Transfer for Manufacture":
					item_dict = self.get_pending_raw_materials(backflush_based_on)
					if self.to_warehouse and self.pro_doc:
						for item in item_dict.values():
							item["to_warehouse"] = self.pro_doc.wip_warehouse
					self.add_to_stock_entry_detail(item_dict)

				elif (
					self.work_order
					and (
						self.purpose == "Manufacture"
						or self.purpose == "Material Consumption for Manufacture"
					)
					and not self.pro_doc.skip_transfer
					and self.flags.backflush_based_on == "Material Transferred for Manufacture"
				):
					self.add_transfered_raw_materials_in_items()

				elif (
					self.work_order
					and (
						self.purpose == "Manufacture"
						or self.purpose == "Material Consumption for Manufacture"
					)
					and self.flags.backflush_based_on == "BOM"
					and frappe.db.get_single_value("Manufacturing Settings", "material_consumption") == 1
				):
					self.get_unconsumed_raw_materials()

				else:
					if not self.fg_completed_qty:
						frappe.throw(_("Manufacturing Quantity is mandatory"))

					item_dict = {}

					# # Get Subcontract Order Supplied Items Details
					# if (
					# 	self.get(self.subcontract_data.order_field)
					# 	and self.purpose == "Send to Subcontractor"
					# ):
					# 	# Get Subcontract Order Supplied Items Details
					# 	parent = frappe.qb.DocType(self.subcontract_data.order_doctype)
					# 	child = frappe.qb.DocType(self.subcontract_data.order_supplied_items_field)

					# 	item_wh = (
					# 		frappe.qb.from_(parent)
					# 		.inner_join(child)
					# 		.on(parent.name == child.parent)
					# 		.select(child.rm_item_code, child.reserve_warehouse)
					# 		.where(parent.name == self.get(self.subcontract_data.order_field))
					# 	).run(as_list=True)

					# 	item_wh = frappe._dict(item_wh)

					# for original_item, item in item_dict.items():
					# 	if self.pro_doc and cint(self.pro_doc.from_wip_warehouse):
					# 		item["from_warehouse"] = self.pro_doc.wip_warehouse
					# 	# Get Reserve Warehouse from Subcontract Order
					# 	if (
					# 		self.get(self.subcontract_data.order_field)
					# 		and self.purpose == "Send to Subcontractor"
					# 	):
					# 		item["from_warehouse"] = item_wh.get(item.item_code)
					# 	item["to_warehouse"] = (
					# 		self.to_warehouse if self.purpose == "Send to Subcontractor" else ""
					# 	)

					# 	if original_item != item.get("item_code"):
					# 		item["original_item"] = original_item
    
					if self.pro_doc and self.pro_doc.doctype == "Work Order":
						for wo_item in self.pro_doc.get("required_items", []):
							if wo_item.item_code not in item_dict:
								from_warehouse=frappe.db.get_value("Serial No",wo_item.custom_serial_number,"warehouse")
								item_dict[wo_item.item_code] = {
									"item_code": wo_item.item_code,
									"qty": wo_item.required_qty,
									"uom": wo_item.stock_uom,
                                    "s_warehouse":from_warehouse,
									"to_warehouse": "",
                                    "serial_no": wo_item.custom_serial_number
								}	
							else:
								if wo_item.custom_serial_number:
									item_dict[wo_item.item_code]["serial_no"] = wo_item.custom_serial_number
                                                                            

					self.add_to_stock_entry_detail(item_dict)

			# fetch the serial_no of the first stock entry for the second stock entry
			if self.work_order and self.purpose == "Manufacture":
				work_order = frappe.get_doc("Work Order", self.work_order)
				add_additional_cost(self, work_order)

			# add finished goods item
			if self.purpose in ("Manufacture", "Repack"):
				self.set_process_loss_qty()
				self.load_items_from_bom()

		self.set_scrap_items()
		self.set_actual_qty()
		self.validate_customer_provided_item()
		self.calculate_rate_and_amount(raise_error_if_no_rate=False)