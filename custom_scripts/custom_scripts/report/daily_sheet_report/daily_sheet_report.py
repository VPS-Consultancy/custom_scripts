# Copyright (c) 2013, C.R.I.O and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	if filters:
		columns = get_column()
		data = get_data(filters)
	return columns, data

def get_column():
	columns = [
		{
		"label": "Voucher Type",
		"fieldname": "voucher_type",
		"fieldtype": "Data",
		"width": 200
	},
		{
		"label": "Voucher No",
		"fieldname": "voucher_no",
		"fieldtype": "Dynamic Link",
		"options": "voucher_type",
		"width": 200
	},
	{
		"label": "Payment Mode",
		"fieldname": "payment_mode",
		"fieldtype": "Data",
		"width": 200
	},
	{
		"label": "Payment Type",
		"fieldname": "payment_type",
		"fieldtype": "Data",
		"width": 200
	},
	{
		"label": "Amount",
		"fieldname": "amount",
		"fieldtype": "Currency",
		"width": 200
	},
	{
		"label": "Remarks",
		"fieldname": "remarks",
		"fieldtype": "Data",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]
	# si_list = frappe.db.sql('''select %s as invoice_type, si.name as invoice, si.base_grand_total - si.outstanding_amount as received_amount, 0 as paid_amount
	# 	from `tabSales Invoice` si where si.posting_date between %s and %s and si.docstatus = 1''',('Sales Invoice',filters['cf_from_date'],filters['cf_to_date']),  as_dict = True)
	pos_list = frappe.db.sql('''select %s as voucher_type, pi.name as voucher_no, sip.mode_of_payment as payment_mode, sip.base_amount as amount, 0 as paid_amount
		from `tabPOS Invoice` pi join `tabSales Invoice Payment` sip
		on sip.parent = pi.name
		where pi.posting_date between %s and %s and pi.docstatus = 1''',('POS Invoice',filters['cf_date'],filters['cf_date']),  as_dict = True)

	pe_list = frappe.db.sql('''select %s as voucher_type, pe.name as voucher_no, pe.paid_amount as amount, pe.remarks as remarks,
		pe.mode_of_payment as payment_mode, pe.payment_type as payment_type
		from `tabPayment Entry` pe 
		where pe.posting_date  between %s and %s and pe.docstatus = 1''',('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	je_list = frappe.db.sql('''select  %s as voucher_type, je.name as voucher_no, je.total_debit as amount, je.remark as remarks
		from `tabJournal Entry` je 
		where je.voucher_type = 'Cash Entry' and  je.posting_date  between %s and %s and je.docstatus = 1''',('Journal Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	data = pos_list + pe_list + je_list 
	
	data += calculate_amount(data,filters)

	return data


def calculate_amount(entries,filters):
	total_sales = 0
	closing_cash = filters['cf_opening_balance'] if 'cf_opening_balance' in filters else 0
	
	total_sales = sum([entry['amount'] for entry in entries if entry['voucher_type'] == 'POS Invoice' or (entry['voucher_type'] == 'Payment Entry' and entry['payment_type'] == 'Receive')])
	
	closing_cash += sum([entry['amount'] for entry in entries if (entry['voucher_type'] == 'POS Invoice' and entry['payment_mode'] == 'Cash') or (entry['voucher_type'] == 'Payment Entry' and entry['payment_type'] == 'Receive' and entry['payment_mode'] == 'Cash')]) - \
	sum([entry['amount'] for entry in entries if (entry['voucher_type'] == 'Journal Entry') or (entry['voucher_type'] == 'Payment Entry' and entry['payment_type'] == 'Pay' and entry['payment_mode'] == 'Cash')])

	if frappe.db.exists('Daily Balance',{'date':filters['cf_date']}):
		frappe.db.set_value('Daily Balance',{'date':filters['cf_date']},'amount',closing_cash)
	else:
		frappe.get_doc({'doctype':'Daily Balance', 'date':filters['cf_date'],'amount':closing_cash}).insert()
	
	frappe.db.commit()
	
	return [{'payment_type':frappe.bold('Closing Cash'),'amount':closing_cash},{'payment_type':frappe.bold('Total Sales'),'amount':total_sales}]