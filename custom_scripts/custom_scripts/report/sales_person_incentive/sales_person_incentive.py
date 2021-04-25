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
		"width": 150
	},
		{
		"label": "Invoice",
		"fieldname": "invoice",
		"fieldtype": "Dynamic Link",
		"options": "invoice_type",
		"width": 200
	},
	{
		"label": "Customer",
		"fieldname": "customer",
		"fieldtype": "Data",
		"width": 200
	},
	{
		"label": "Grand Total",
		"fieldname": "grand_total",
		"fieldtype": "Currency",
		"width": 160
	},
	{
		"label": "Received Amount",
		"fieldname": "received_amount",
		"fieldtype": "Currency",
		"width": 160
	},
	{
		"label": "Sales Person",
		"fieldname": "sales_person",
		"fieldtype": "Link",
		"options":"Sales Person",
		"width": 170
	},
	{
		"label": "Incentive",
		"fieldname": "sincentive",
		"fieldtype": "Currency",
		"width": 100
	},
	{
		"label": "Status",
		"fieldname": "status",
		"fieldtype": "Data",
		"width": 100
	}
	]
	return columns

def get_data(filters):
	data =[]

	if 'cf_sales_person' not in filters:
		si_list = frappe.db.sql('''select "Sales Invoice" as invoice_type, 
						si.name as invoice, si.status as status,
						si.rounded_total - si.outstanding_amount as received_amount,
						sp.sales_person as sales_person , si.rounded_total * (sp.commission_rate / 100) as sincentive,
						si.rounded_total as grand_total, si.customer as customer
						from `tabSales Invoice` si left join `tabSales Team` sp on sp.parent = si.name 
						where si.posting_date between %s and %s and si.docstatus = 1''',
						(filters['cf_from_date'],filters['cf_to_date']), as_dict = True)
		
		pos_list = frappe.db.sql('''select "POS Invoice" as invoice_type, pi.name as invoice, 
						pi.paid_amount as received_amount, pi.status as status,
						sp.sales_person as sales_person, pi.rounded_total * (sp.commission_rate / 100) as sincentive,
						pi.customer as customer, pi.rounded_total as grand_total
						from `tabSales Team` sp left join `tabPOS Invoice` pi on sp.parent = pi.name 
						where pi.posting_date between %s and %s and pi.docstatus = 1''',
						(filters['cf_from_date'],filters['cf_to_date']), as_dict = True)

		data = si_list + pos_list
	else:
		filtered_sales_invoice = frappe.db.sql('''select "Sales Invoice" as invoice_type, si.name as invoice,
									si.rounded_total - si.outstanding_amount as received_amount,
									sp.sales_person as sales_person, si.rounded_total * (sp.commission_rate / 100) as sincentive,
									si.status as status,si.rounded_total as grand_total,
									si.customer as customer
									from `tabSales Team` sp join `tabSales Invoice` si on sp.parent = si.name 
									where sp.sales_person = %s and  si.posting_date between %s and %s and si.docstatus = 1''',
									(filters['cf_sales_person'],filters['cf_from_date'],filters['cf_to_date']), as_dict = True)

		filtered_pos_invoice = frappe.db.sql('''select "POS Invoice" as invoice_type, pi.name as invoice,
									pi.paid_amount as received_amount, sp.sales_person as sales_person,
									pi.rounded_total * (sp.commission_rate / 100) as sincentive, pi.status as status, pi.customer as customer,
									pi.rounded_total as grand_total
									from `tabSales Team` sp join `tabPOS Invoice` pi on sp.parent = pi.name
									where sp.sales_person = %s and pi.posting_date between %s and %s and pi.docstatus = 1''',
									(filters['cf_sales_person'],filters['cf_from_date'],filters['cf_to_date']), as_dict = True)

		data = filtered_sales_invoice + filtered_pos_invoice

	return data