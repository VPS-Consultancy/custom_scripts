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
		"label": "Invoice",
		"fieldname": "sales_invoice",
		"fieldtype": "Data",
		"width": 200
	},
	{
		"label": "Received Amount",
		"fieldname": "received_amount",
		"fieldtype": "Currency",
		"width": 200
	},
	{
		"label": "Expense",
		"fieldname": "expense",
		"fieldtype": "Data",
		"width": 200
	},
	{
		"label": "Paid Amount",
		"fieldname": "paid_amoutn",
		"fieldtype": "Currency",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]

	if 'cf_sales_person' not in filters:
		si_pe_list = frappe.db.sql('''select si.name, si.base_grand_total - si.outstanding_amount, pe.name, pe.paid_amount
			from `tabSales Invoice` si , `tabPayment Entry` pe 
			where pe.payment_type = "Pay" and si.posting_date between %s and %s ''',(filters['cf_from_date'],filters['cf_to_date']))
		pos_je_list = frappe.db.sql('''select pi.name, pi.paid_amount, je.name, je.total_debit
			from `tabPOS Invoice` pi, `tabJournal Entry` je 
			where pi.posting_date between %s and %s ''',(filters['cf_from_date'],filters['cf_to_date']))

		data = si_pe_list + pos_je_list
		
	return data