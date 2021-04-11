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
		"label": "Invoice Type",
		"fieldname": "invoice_type",
		"fieldtype": "Data",
		"width": 200
	},
		{
		"label": "Invoice",
		"fieldname": "invoice",
		"fieldtype": "Dynamic Link",
		"options": "invoice_type",
		"width": 200
	},
	{
		"label": "Received Amount",
		"fieldname": "received_amount",
		"fieldtype": "Currency",
		"width": 200
	},
	{
		"label": "Expense Type",
		"fieldname": "expense_type",
		"fieldtype": "Data",
		"width": 200
	},
		{
		"label": "Expense",
		"fieldname": "expense",
		"fieldtype": "Dynamic Link",
		"options": "expense_type",
		"width": 200
	},
	{
		"label": "Paid Amount",
		"fieldname": "paid_amount",
		"fieldtype": "Currency",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]
	si_list = frappe.db.sql('''select %s as invoice_type, si.name as invoice, si.base_grand_total - si.outstanding_amount as received_amount
		from `tabSales Invoice` si where si.posting_date between %s and %s and si.docstatus = 1''',('Sales Invoice',filters['cf_from_date'],filters['cf_to_date']),  as_dict = True)
	pos_list = frappe.db.sql('''select %s as invoice_type, pi.name as invoice, pi.paid_amount as received_amount
		from `tabPOS Invoice` pi 
		where pi.posting_date between %s and %s and pi.docstatus = 1''',('POS Invoice',filters['cf_from_date'],filters['cf_to_date']),  as_dict = True)
	pe_list = frappe.db.sql('''select %s as expense_type, pe.name as expense, pe.paid_amount as paid_amount
		from `tabPayment Entry` pe 
		where pe.payment_type = "Pay" and pe.posting_date  between %s and %s and pe.docstatus = 1''',('Payment Entry',filters['cf_from_date'],filters['cf_to_date']),  as_dict = True)
	je_list = frappe.db.sql('''select  %s as expense_type, je.name as expense, je.total_debit as paid_amount
		from `tabJournal Entry` je 
		where je.posting_date  between %s and %s and je.docstatus = 1''',('Journal Entry',filters['cf_from_date'],filters['cf_to_date']),  as_dict = True)
	data = si_list + pos_list + je_list + pe_list
	return data