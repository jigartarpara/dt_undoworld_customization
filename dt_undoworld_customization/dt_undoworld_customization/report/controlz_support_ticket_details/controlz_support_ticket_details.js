frappe.query_reports["ControlZ Support Ticket Details"] = {
    filters: [
        {
            fieldname: "ticket_id",
            label: "Ticket ID",
            fieldtype: "Link",
			options:"Support Ticket",
            reqd: 0
        },
        {
            fieldname: "serial_number",
            label: "Serial Number",
            fieldtype: "Link",
			options:"Support Ticket",
            reqd: 0
        }
    ]
};
