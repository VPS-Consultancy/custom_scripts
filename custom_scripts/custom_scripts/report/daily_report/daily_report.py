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
		"label": "Sales Invoice",
		"fieldname": "sales_invoice",
		"fieldtype": "Link",
		"options":"Sales Invoice",
		"width": 200
	},
	{
		"label": "POS Invoice",
		"fieldname": "pos_invoice",
		"fieldtype": "Link",
		"options":"POS Invoice",
		"width": 200
	},
	{
		"label": "Received Amount",
		"fieldname": "received_amount",
		"fieldtype": "Currency",
		"width": 200
	}]
	return columns

def get_data(filters):
	data =[]

	if 'cf_sales_person' not in filters:
		sales_invoice_list = frappe.db.get_list('Sales Invoice',filters=[['posting_date' ,'>=',filters['cf_from_date']],
			['posting_date' ,'<=',filters['cf_to_date']]],fields=['name','base_grand_total','outstanding_amount'])
		pos_invoice_list = frappe.db.get_list('POS Invoice',filters=[['posting_date' ,'>=',filters['cf_from_date']],
			['posting_date' ,'<=',filters['cf_to_date']]],fields=['name','paid_amount'])
		data = [{'sales_invoice':inv['name'],'pos_invoice':'', 'received_amount':inv['base_grand_total']-inv['outstanding_amount']} for inv in  sales_invoice_list]
		data.extend( [{'sales_invoice':'','pos_invoice':inv['name'], 'received_amount':inv['paid_amount']} for inv in  pos_invoice_list])
	else:
		filtered_sales_invoice = frappe.db.sql(
			'''select si.name as sales_invoice, "" as pos_invoice , si.base_grand_total - si.outstanding_amount as received_amount
			from `tabSales Team` sp,
			`tabSales Invoice` si where sp.parenttype = "Sales Invoice" 
			and sp.sales_person = %s and sp.parent = si.name ''',filters['cf_sales_person'])
		filtered_pos_invoice = frappe.db.sql(
			'''select "" as sales_invoice, pi.name as pos_invoice , pi.paid_amount as received_amount
			from `tabSales Team` sp,
			`tabPOS Invoice` pi where sp.parenttype = "POS Invoice" 
			and sp.sales_person = %s and sp.parent = pi.name ''',filters['cf_sales_person'])

		data = filtered_sales_invoice + filtered_pos_invoice
	return data