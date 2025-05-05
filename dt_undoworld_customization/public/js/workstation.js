frappe.ui.form.on('Workstation', {
    validate: function(frm) {
        if (frm.doc.custom_is_first_workstation) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Workstation",
                    filters: {
                        custom_is_first_workstation: 1,
                        name: ["!=", frm.doc.name]
                    },
                    fields: ["name"]
                },
                callback: function(response) {
                    // If there is another record with custom_is_first_workstation checked
                    if (response.message && response.message.length > 0) {
                        frappe.show_alert({
                            message:__('Only one workstation can be marked as the First Workstation.'),
                            indicator:'red'
                        }, 5);
                        frm.set_value('custom_is_first_workstation', 0); // Uncheck the box
                    }
                }
            });
        }
    }
});
