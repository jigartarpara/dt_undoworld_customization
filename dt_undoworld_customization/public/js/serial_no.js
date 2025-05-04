frappe.ui.form.on('Serial No', {
    refresh: function(frm) {
        if (frm.doc.warehouse === "Renew Hub - UW" || frm.doc.warehouse === "Old Parts Warehouse - UW") {
        frm.page.set_secondary_action(__('Create BOM'), function(){
            let d = new frappe.ui.Dialog({
                title: 'Please Select the Finished Good',
                fields: [
                    {
                        label: 'Finished Good',
                        fieldname: 'finished_good',
                        fieldtype: 'Link',
                        options: 'Item',
                    }
                ],
                size: 'small',
                primary_action_label: 'Create BOM',
                primary_action(values){
                    d.hide();
                    console.log(frm.doc.name);
                    frappe.new_doc('BOM',{},
                        doc =>{
                            doc.item = values.finished_good,
                            doc.quantity = 1,
                            frappe.model.clear_table(doc, 'items');
                            let row = frappe.model.add_child(doc, 'items');
                            row.item_code = frm.doc.item_code
                            row.custom_is_old_phone = 1
                            row.qty = 1
                            row.uom = 'Nos'
                            row.custom_serial_no = frm.doc.name
                        }
                    )
                }
                
            })
            d.show();
        }).addClass("btn-primary");
    }
        
    }
})