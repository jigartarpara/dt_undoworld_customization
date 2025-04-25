frappe.ui.form.on('Work Order', {
    onload(frm) {
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
				}
			});
		});
	},  
    refresh: function(frm) {
        if (frm.doc.docstatus === 0 && frm.doc.name) {
            frm.add_custom_button(__('Move to Next Workstation'), function() {
                // Create a dialog with a dropdown for selecting a workstation
                let dialog = new frappe.ui.Dialog({
                    title: __('Select Workstation'),
                    fields: [
                        {
                            fieldtype: 'Select',
                            label: __('Workstation'),
                            fieldname: 'workstation',
                            options: ['','L1', 'L2', 'L3', 'L4'],  // Add all workstation options here
                            reqd: 1
                        }
                    ],
                    primary_action: function() {
                        let selected_workstation = dialog.get_values().workstation;
                        // Call the backend method to move to the selected workstation
                        frappe.call({
                            method: "dt_undoworld_customization.public.py.work_order.move_to_next_workstation",
                            args: {
                                work_order_name: frm.doc.name,
                                selected_workstation: selected_workstation  // Pass the selected workstation
                            },
                            callback: function(r) {
                                if (!r.exc) {
                                    frappe.msgprint(r.message || "Moved to next workstation.");
                                    frm.reload_doc();
                                }
                            }
                        });
                        dialog.hide();  // Hide dialog after submission
                    },
                    primary_action_label: __('Move')
                });
    
                dialog.show();  // Show the dialog
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
