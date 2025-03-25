# Copyright (c) 2024, DTPL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from requests import post,get
import json
from frappe.utils import now,time_diff_in_hours, today,add_to_date

class PhonecheckSettings(Document):
    def before_save(self):
        pwd = self.get_password('password')
        token = create_token(self.username, pwd)
        if token != 0:
            self.token = token
            self.token_creation_datetime = now()
            
    def get_token(self):
        if (self.token == None) or (self.token == ''):
            self.save()
            return self.token
        if check_token(self.token, self.token_creation_datetime) == 1:
            return self.token
        self.save()
        return self.token


def create_token(usr, pwd):
    url = 'https://api.phonecheck.com/v2/auth/master/login'
    request = {
    "username": usr,
    "password": pwd
	}
    request = json.dumps(request)
    headers = {"Content-Type": "application/json"}
    response = post(url= url,headers=headers, data= request)
    if response.status_code == 200:
        response = response.json()
        return (response['token'])
    return 0
        
def testing():
    usr = 'sgcmobility'
    pwd = '0of9ytovlh'
    print('\n\n\n\n')
    create_token(usr,pwd)

def check_token(token, create_datetime):
    if time_diff_in_hours(now(), create_datetime) > 24:
        return 0
    return 1

@frappe.whitelist()
def fetch_device_details(date):
    # print('\n\n\n\n')
    settings_doc = frappe.get_doc('Phonecheck Settings')
    token = settings_doc.get_token()
    url = 'https://api.phonecheck.com/v2/master/all-devices'
    headers = {
        		"Content-Type": "application/json",
          		"token_master": token
            }
    request = {
				"startdate": date,
				"enddate": date
			}
    doc = frappe.new_doc('Phonecheck Log')
    doc.posting_date = today()
    doc.url =url
    doc.request_json = str(request)
    request = json.dumps(request)
    response = post(url= url,headers=headers, data= request)
    # print(response)
    # return 1
    if response.status_code == 200:
        response = response.json()
        map_details_to_table(response['devices'], doc)
        doc.response_json = str(response)
        doc.save()
        doc.submit()
        return 1
    response = response.json()
    doc.response_json = str(response)
    doc.submit()
    



def map_details_to_table(devices, doc):
    print('\n\n\n\n')
    for device in devices:
        # print (device)
        # print ('\n\n\n\n\nn\n-------------------------------------')
        row = {
			'imei': device['imei'],
			'imei2': device['imei2'],
			'ram': device['ram'],
			'memory': device['memory'],
			'model_name': device['model'],
			'model_no': device['modelNo'],
			'serial': device ['serial'],
			'udid': device['udid'],
			'itemsku_serial_no': device['skuCode'],
            'remarks': device['failedTests']
		}
        if device['working'] == 'Yes':
            row['quality_test'] = 1            
        
        doc.append('items', row)