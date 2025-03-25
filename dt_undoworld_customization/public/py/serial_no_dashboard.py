from frappe import _


def get_data(data):
	return {
		"fieldname": "serial_no",
		"non_standard_fieldnames": {
            "BOM": "custom_serial_no",
			"Quality Inspection": "item_serial_no",
		},		
	
		"transactions": [
            { "items": [ "Delivery Note", "BOM", "Stock Entry", "Serial and Batch Bundle", "Quality Inspection" ] }
        ],
	}