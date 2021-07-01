from __future__ import unicode_literals
import frappe, json
import requests
from erpnext.accounts.party import get_dashboard_info


def get_mobile_number(customer):

    customer_mobile_no = frappe.db.sql(
        """
		SELECT `tabContact`.mobile_no
		FROM `tabContact`, `tabDynamic Link`
		WHERE
		`tabDynamic Link`.parent = `tabContact`.name and
		`tabDynamic Link`.parenttype = 'Contact' and
		`tabDynamic Link`.link_doctype = 'Customer' and
		`tabDynamic Link`.link_name = %(customer)s""",
        {"customer": customer},
        as_dict=True,
    )

    return customer_mobile_no


def sms_gateway(user, password, sender_id, mobile_number, message):
    url = f"http://admagister.net/api/mt/SendSMS?user={user}&password={password}&senderid={sender_id}&channel=Trans&DCS=0&flashsms=0&number={mobile_number}&text={message}&route=6"
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers)
    return response


@frappe.whitelist()
def send_sms(customer, invoice_no, due_date, amount):
    mobile_number = (get_mobile_number(customer))[0]["mobile_no"]
    settings = frappe.get_single("Nirmala Settings")
    user = settings.user
    sender_id = settings.sender_id
    password = frappe.utils.password.get_decrypted_password(
        "Nirmala Settings", settings.name, fieldname="password"
    )
    mobile_number = "91" + mobile_number
    outstanding_amt = (get_dashboard_info("Customer", customer))[0]["total_unpaid"]
    message = f"Nirmala Enterprises Alert. Dear Customer, \
				Invoice No. {invoice_no} of Rs.{amount} \
				was generated on {due_date}. \
				Total outstanding amount as of today is {outstanding_amt} ."
    result = sms_gateway(user, password, sender_id, mobile_number, message)
    if result.status_code == 200:
        res_json = json.loads(result.text)
        if res_json["ErrorCode"] == "000":
            return True
    return False
