import frappe
import requests
from frappe.model.document import Document
import base64


def before_validate(self, method):
    if self.custom_order_status == 'Fulfiled':
        if self.get('custom_order_status') == "Fulfiled" and self.get_db_value('custom_order_status') != 'Fulfiled':

            custom_mobile_number = "+91"+str(self.custom_mobile_number)
            print(custom_mobile_number)
            if not custom_mobile_number:
                return
            
            bik_settings = frappe.get_single('BIK Customer API Settings')

            api_key = bik_settings.key
            secret_key = bik_settings.secret
            app_id = bik_settings.app_id
            template_id = bik_settings.template_id 
            api_url=bik_settings.api_url

            token = f"{api_key}:{secret_key}"
            base64_token = base64.b64encode(token.encode()).decode()

            attachment = frappe.get_all('File', filters={
                'attached_to_doctype': 'Sales Order',
                'attached_to_name': self.name
            }, fields=['file_url'])

            if attachment:
                # Assuming the first attachment is the one you want to send
                file_url = "https://controlz.thecodeforge.in"+attachment[0].file_url
            else:
                file_url = None 

            # API URL
            url = api_url
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic '+base64_token
            }

            data = {
                "appId":app_id,
                "contactIdentifier": custom_mobile_number,
                "medium": "whatsapp",
                "payload": {
                    "templateId": template_id,
                    "components": {
                        "body": [
                        file_url
                        ],
                       
                    }
                }
            }

            # Make the API call
            response = requests.post(url, headers=headers, json=data)
            print(response.text)
            # Handle the response
            if response.status_code == 200:
                frappe.msgprint("API call successful!")
            else:
                frappe.log_error("Failed to call BIK API", response.text)
                frappe.msgprint(f"Failed to call BIK API. Status code: {response.status_code}")
