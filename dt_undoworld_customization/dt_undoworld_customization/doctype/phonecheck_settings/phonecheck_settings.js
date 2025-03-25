// Copyright (c) 2024, DTPL and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Phonecheck Settings", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Phonecheck Settings", "fetch_devices_details", function(frm) {

    let d = new frappe.ui.Dialog({
        title: 'Select Date',
        fields: [
            {
                label: 'Date',
                fieldname: 'date',
                fieldtype: 'Date'
            },
        ],
        size: 'small',
        primary_action_label: 'Fetch Device Details',
        primary_action(values){
            d.hide();
            frappe.call({
                method: 'dt_undoworld_customization.dt_undoworld_customization.doctype.phonecheck_settings.phonecheck_settings.fetch_device_details',
                args: {'date': values.date},
                callback: function(r){
                    if (r.message == 0){}
                    else{
                        frappe.show_alert('Device details has been fetched', 5)
                    }
                }
            })
        }
    })
    d.show();
    cur_frm.reload_doc();

    // console.log(frm.doc.customer)
    // frappe.call({
    //     method: 'dt_undoworld_customization.dt_undoworld_customization.doctype.phonecheck_settings.phonecheck_settings.fetch_device_details',
    // callback: function(r) {
	//   if (r.message == 0){

	//   } else {
    //   frappe.show_alert('Device details has been fetched', 5);
	// } 
    //   cur_frm.reload_doc();
    // }
    // });
    

});