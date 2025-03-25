frappe.ui.form.on('Stock Entry',{
    custom_change_fg_item: function(frm) {

        if (!frm.is_new()) {
            let old_fg_row = {}
            frm.doc.items.forEach(function(row){
                if (row.is_finished_item === 1){
                    old_fg_row = row
                }
            })
            let d = new frappe.ui.Dialog({
                title: 'Enter the new FG Item Code',
                fields: [
                    {
                        label: 'FG Item Code',
                        fieldname: 'fg_item_code',
                        fieldtype: 'Link',
                        options: 'Item'
                    }
                ],
                size: 'small',
                primary_action_label: 'Change FG Item',
                primary_action(values){
                    d.hide();
                    frappe.confirm('Are you sure you want to change the FG Item and submit this stock entry?',
                        () => {
                            frappe.call({
                                method: 'dt_undoworld_customization.public.py.stock_entry.se_for_new_fg',
                                args: {
                                    'old_se_name': frm.doc.name,
                                    'old_fg_row': old_fg_row,
                                    'new_fg_item_code': values.fg_item_code
                                },
                                callback: function (r){
                                    if (r.message == 1){
                                        doc.refresh()
                                        // frappe.show_alert({
                                        //     message:__('Stock Entry with New FG created and submitted'),
                                        //     indicator:'green'
                                        // }, 5);
                                        // console.log(r.message)
                                    }
                                }
                            })
                        }, () => {
                            doc.refresh()                   // action to perform if No is selected
                        })

                }
            })
            d.show()
        }
        else{
            frappe.throw('Please save the document first')
        }
    }
})