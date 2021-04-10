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
		"label": "Sales Person",
		"fieldname": "sales_person",
		"fieldtype": "Link",
		"options":"Sales Person",
		"width": 200
	},
	{
		"label": "Incentive",
		"fieldname": "sincentive",
		"fieldtype": "Currency",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]

	if 'cf_sales_person' not in filters:
		si_pe_list = frappe.db.sql('''select si.name as sales_invoice, si.base_grand_total - si.outstanding_amount as received_amount,
			sp.sales_person, sp.incentives
			from `tabSales Invoice` si join `tabSales Team` sp on sp.parent = si.name  where si.posting_date between %s and %s ''',(filters['cf_from_date'],filters['cf_to_date']))
		pos_je_list = frappe.db.sql('''select pi.name as pos_invoice , pi.paid_amount as received_amount, 
			sp.sales_person, sp.incentives
			from `tabSales Team` sp join
			`tabPOS Invoice` pi on sp.parent = pi.name where pi.posting_date between %s and %s ''',(filters['cf_from_date'],filters['cf_to_date']))

		data = si_pe_list + pos_je_list
	else:
		filtered_sales_invoice = frappe.db.sql(
			'''select si.name as sales_invoice, si.base_grand_total - si.outstanding_amount as received_amount, sp.sales_person, sp.incentives
			from `tabSales Team` sp join `tabSales Invoice` si on sp.parent = si.name 
			where sp.sales_person = %s and  si.posting_date between %s and %s ''',(filters['cf_sales_person'],filters['cf_from_date'],filters['cf_to_date']))
		filtered_pos_invoice = frappe.db.sql(
			'''select pi.name as pos_invoice , pi.paid_amount as received_amount, sp.sales_person, sp.incentives
			from `tabSales Team` sp join `tabPOS Invoice` pi on sp.parent = pi.name
			where sp.sales_person = %s and pi.posting_date between %s and %s ''',(filters['cf_sales_person'],filters['cf_from_date'],filters['cf_to_date']))

		data = filtered_sales_invoice + filtered_pos_invoice
	return data