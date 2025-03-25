import frappe

@frappe.whitelist()
def add_device_details():
    if frappe.request.method != 'POST':
        return("Method Not Allowed. Please use POST method")
    request = frappe.request.get_json()

    response = validate_response(request)
    if response != 1:
        return response
    
    add_detail_to_serial_no(response ,request['imei1'], request['imei2'],request['eid'], request['sn'])



def validate_response(request):
    pass


def add_detail_to_serial_no(serial_no, imei1, imei2, eid, sn):
    doc = frappe.get_doc('Serial No', serial_no)

    doc.custom_imei1 = imei1
    doc.custom_imei2 = imei2
    doc.custom_eid = eid
    doc.custom_sn = sn
    doc.save()