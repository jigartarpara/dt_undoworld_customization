import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Ticket ID", "fieldname": "ticket_id", "fieldtype": "Link","options":"Support Ticket", "width": 150},
        {"label": "Serial Number", "fieldname": "serial_number", "fieldtype": "Link","options":"Serial No", "width": 150},
        {"label": "Claim Time", "fieldname": "claim_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Approval Time", "fieldname": "approval_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Pickup Arrange Time", "fieldname": "pickup_arrange_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Pickup Time", "fieldname": "pickup_time", "fieldtype": "Datetime", "width": 150},
        {"label": "In Transit Time", "fieldname": "in_transit_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Device Received Time", "fieldname": "device_received_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Dispatch Time", "fieldname": "dispatch_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Delivery Time", "fieldname": "delivery_time", "fieldtype": "Datetime", "width": 150},
        {"label": "Complete Time", "fieldname": "complete_time", "fieldtype": "Datetime", "width": 150},
    ]

    # Build conditions based on filters
    conditions = {}
    if filters.get("ticket_id"):
        conditions["name"] = filters["ticket_id"]
    if filters.get("serial_number"):
        conditions["serial_number"] = filters["serial_number"]

    tickets = frappe.get_all("Support Ticket", filters=conditions, fields=["name", "serial_number"])

    data = []

    for ticket in tickets:
        status_rows = frappe.get_all(
            "Status Tracking",
            filters={"parent": ticket.name},
            fields=["status", "posting_date"]
            )

        status_map = {}
        for row in status_rows:
            if row.status not in status_map:
                status_map[row.status] = row.posting_date

        data.append({
            "ticket_id": ticket.name,
            "serial_number": ticket.serial_number,
            "claim_time": status_map.get("Pending"),
            "approval_time": status_map.get("Approved"),
            "pickup_arrange_time": status_map.get("Pick Arranged"),
            "pickup_time": status_map.get("Pick Up"),  # if used
            "in_transit_time": status_map.get("In Transit"),
            "device_received_time": status_map.get("Device Received"),
            "dispatch_time": status_map.get("Device Out for Delivery"),
            "delivery_time": status_map.get("Waiting For Delivery Arrange"),
            "complete_time": status_map.get("Complete"),
        })

    return columns, data
