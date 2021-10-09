from __future__ import unicode_literals
import frappe, json
import requests
from erpnext.accounts.party import get_dashboard_info
import erpnext
from erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log import POSInvoiceMergeLog
from frappe.model.mapper import map_doc, map_child_doc
from frappe.utils import flt

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

def create_log(doc_name, api_method, request, response):
	request_log = frappe.get_doc({
		"doctype": "SMS Request Log",
		"user": frappe.session.user,
		"reference_document":doc_name,
		"api_method": api_method,
		"response": response,
		"request": request
	})
	request_log.save(ignore_permissions=True)
	frappe.db.commit()

def sms_gateway(user, password, sender_id, mobile_number, message, doc_name):
	url = f"http://admagister.net/api/mt/SendSMS?user={user}&password={password}&senderid={sender_id}&channel=Trans&DCS=0&flashsms=0&number={mobile_number}&text={message}&route=37"
	headers = {"Content-Type": "application/json"}
	response = requests.request("GET", url, headers=headers)
	request_params = f'User: {user}, Sender ID: {sender_id}, Mobile No: {mobile_number}, Message: {message} URL: {url}'
	res = f'Status code: {response.status_code}, Response - {json.loads(response.text)}'
	create_log(doc_name, 'Send SMS', request_params, res)
	return response

@frappe.whitelist()
def send_sms(customer, invoice_no, inv_date, amount):
	mobile_number = (get_mobile_number(customer))[0]["mobile_no"]
	settings = frappe.get_single("Nirmala Settings")
	user = settings.user
	sender_id = settings.sender_id
	password = frappe.utils.password.get_decrypted_password(
		"Nirmala Settings", settings.name, fieldname="password"
	)
	mobile_number = "91" + mobile_number
	outstanding_amt = (get_dashboard_info("Customer", customer))[0]["total_unpaid"]
	message = "Dear Customer, Invoice {} of Rs.{} was generated on {}. Outstanding amt: Rs.{} Thanks. Have a great day! - Team Nirmala Home mart".format(invoice_no, amount, inv_date, outstanding_amt)
	result = sms_gateway(user, password, sender_id, mobile_number, message, invoice_no)
	if result.status_code == 200:
		res_json = json.loads(result.text)
		if res_json["ErrorCode"] == "000":
			return True
	return False

class ERPNextPOSInvoiceMergeLog(POSInvoiceMergeLog):
	def merge_pos_invoice_into(self, invoice, data):
		items, payments, taxes = [], [], []
		loyalty_amount_sum, loyalty_points_sum, discount_amt = 0, 0, 0
		for doc in data:
			map_doc(doc, invoice, table_map={ "doctype": invoice.doctype })

			if doc.redeem_loyalty_points:
				invoice.loyalty_redemption_account = doc.loyalty_redemption_account
				invoice.loyalty_redemption_cost_center = doc.loyalty_redemption_cost_center
				loyalty_points_sum += doc.loyalty_points
				loyalty_amount_sum += doc.loyalty_amount
			
			invoice.apply_discount_on = doc.apply_discount_on
			invoice.additional_discount_percentage = doc.additional_discount_percentage
			discount_amt += doc.discount_amount

			for item in doc.get('items'):
				found = False
				for i in items:
					if (i.item_code == item.item_code and not i.serial_no and not i.batch_no and
						i.uom == item.uom and i.net_rate == item.net_rate):
						found = True
						i.qty = i.qty + item.qty

				if not found:
					item.price_list_rate = 0
					si_item = map_child_doc(item, invoice, {"doctype": "Sales Invoice Item"})
					items.append(si_item)

			for tax in doc.get('taxes'):
				found = False
				for t in taxes:
					if t.account_head == tax.account_head and t.cost_center == tax.cost_center:
						t.tax_amount = flt(t.tax_amount) + flt(tax.tax_amount_after_discount_amount)
						t.base_tax_amount = flt(t.base_tax_amount) + flt(tax.base_tax_amount_after_discount_amount)
						update_item_wise_tax_detail(t, tax)
						found = True
				if not found:
					taxes.append(tax)

			for payment in doc.get('payments'):
				found = False
				for pay in payments:
					if pay.account == payment.account and pay.mode_of_payment == payment.mode_of_payment:
						pay.amount = flt(pay.amount) + flt(payment.amount)
						pay.base_amount = flt(pay.base_amount) + flt(payment.base_amount)
						found = True
				if not found:
					payments.append(payment)

		if loyalty_points_sum:
			invoice.redeem_loyalty_points = 1
			invoice.loyalty_points = loyalty_points_sum
			invoice.loyalty_amount = loyalty_amount_sum
		
		if discount_amt:
			invoice.discount_amount = discount_amt
		
		invoice.set('items', items)
		invoice.set('payments', payments)
		invoice.set('taxes', taxes)
		invoice.taxes_and_charges = None
		invoice.ignore_pricing_rule = 1

		return invoice

def update_item_wise_tax_detail(consolidate_tax_row, tax_row):
	consolidated_tax_detail = json.loads(consolidate_tax_row.item_wise_tax_detail)
	tax_row_detail = json.loads(tax_row.item_wise_tax_detail)

	if not consolidated_tax_detail:
		consolidated_tax_detail = {}

	for item_code, tax_data in tax_row_detail.items():
		if consolidated_tax_detail.get(item_code):
			consolidated_tax_data = consolidated_tax_detail.get(item_code)
			consolidated_tax_detail.update({
				item_code: [consolidated_tax_data[0], consolidated_tax_data[1] + tax_data[1]]
			})
		else:
			consolidated_tax_detail.update({
				item_code: [tax_data[0], tax_data[1]]
			})

	consolidate_tax_row.item_wise_tax_detail = json.dumps(consolidated_tax_detail, separators=(',', ':'))
