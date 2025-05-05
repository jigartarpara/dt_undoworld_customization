frappe.ui.form.on('Work Order', {
    onload(frm) {

        if (!frm.is_new()) return;

		if (!frm.doc.bom_no || !frm.doc.required_items || !frm.doc.required_items.length) {
			return;
		}
        
		frappe.db.get_doc('BOM', frm.doc.bom_no).then(bom => {
			// Create a map of item_code -> bom_item
			let bom_item_map = {};
			(bom.items || []).forEach(bom_item => {
				bom_item_map[bom_item.item_code] = bom_item;
			});

			(frm.doc.required_items || []).forEach(wo_item => {
				let bom_item = bom_item_map[wo_item.item_code];
				if (bom_item) {
					frappe.model.set_value(wo_item.doctype, wo_item.name, 'custom_is_old_phone', bom_item.custom_is_old_phone || 0);
					frappe.model.set_value(wo_item.doctype, wo_item.name, 'custom_is_part_missing', bom_item.custom_is_part_missing || 0);
                    frappe.model.set_value(wo_item.doctype, wo_item.name, 'custom_serial_number', bom_item.custom_serial_no || "");
				}
			});
		});
	},  
    refresh: function(frm) {
        if (frm.doc.docstatus === 0 && frm.doc.name) {
            frm.add_custom_button(__('Move to Next Workstation'), function() {
                // Fetch workstation names
                frappe.db.get_list('Workstation', {
                    fields: ['name']
                }).then(workstations => {
                    let options = workstations.map(w => w.name);
                    options.unshift(''); // Add blank option

                    // Show dialog
                    let dialog = new frappe.ui.Dialog({
                        title: 'Select Workstation',
                        fields: [{
                            fieldtype: 'Select',
                            label: 'Workstation',
                            fieldname: 'workstation',
                            options: options,
                            reqd: 1
                        }],
                        primary_action_label: 'Move',
                        primary_action(values) {
                            frappe.call({
                                method: "dt_undoworld_customization.public.py.work_order.move_to_next_workstation",
                                args: {
                                    work_order_name: frm.doc.name,
                                    selected_workstation: values.workstation
                                },
                                callback(r) {
                                    if (!r.exc) {
                                        frappe.msgprint(r.message || "Moved to next workstation.");
                                        frm.reload_doc();
                                    }
                                }
                            });
                            dialog.hide();
                        }
                    });

                    dialog.show();
                });
            });
        }
    },

    after_save: function(frm) {
        frappe.show_alert('Moving Items to workstation', 5);
        frappe.call({
            method: "dt_undoworld_customization.public.py.work_order.run_workstation_logic",
            args: {
                work_order_name: frm.doc.name
            },
            callback: function(r) {
                if (!r.exc) {
                    frm.reload_doc();
                }
            }
        });
    },

    before_submit: function (frm) {
        frappe.call({
            method: "dt_undoworld_customization.public.py.work_order.on_submit_work",
            args: {
                work_order_name: frm.doc.name  // Pass the Work Order name
            },
            callback: function (r) {
                if (r.message) {
                    // Show the success message from Python function
                    frappe.msgprint(r.message);
                    frm.reload_doc(); 
                   
                }
            },
            error: function (error) {
                // Handle errors, if any
                frappe.msgprint(__('An error occurred while submitting the Work Order.'));
            }
        });
    }
});



