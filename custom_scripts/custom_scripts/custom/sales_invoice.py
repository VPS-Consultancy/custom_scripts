from __future__ import unicode_literals
import frappe

def get_mobile_number(customer):
	
	customer_mobile_no = frappe.db.sql("""select
		`tabContact`.mobile_no
	from
		`tabContact`, `tabDynamic Link`
	where
		`tabDynamic Link`.parent = `tabContact`.name and
		`tabDynamic Link`.parenttype = 'Contact' and
		`tabDynamic Link`.link_doctype = 'Customer' and
		`tabDynamic Link`.link_name = %(customer)s""", {"customer": customer})
	
	return customer_mobile_no

def send_sms(customer, invoice_no, due_date, amount):
	mobile_number = get_mobile_number(customer)
	settings = frappe.get_single('Nirmala Settings')
	user = settings.user
	senderid = senderid
	password = frappe.utils.password.get_decrypted_password('Nirmala Settings', settings.name, fieldname='password')
	mobile_number = '91'+mobile_number
	message = f'Dear Customer, Invoice No. {invoice_no} of Rs.{amount} was generated. Due Date: {due_date}'
	url = f"http://admagister.net/api/mt/SendSMS?user={user}&password={password}&senderid={senderid}&channel=Trans&DCS=0&flashsms=0&number={mobile_number}&text={message}&route=6"
	headers = {
		"Content-Type": "application/json"
	}
	response = requests.request("GET", url, headers=headers)
	return response