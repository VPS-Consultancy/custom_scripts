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
		"fieldname": "inward_voucher_type",
		"fieldtype": "Data",
		"width": 150
	},
		{
		"label": "Voucher No",
		"fieldname": "voucher_no",
		"fieldtype": "Dynamic Link",
		"options": "inward_voucher_type",
		"width": 200
	},
	{
		"label": "Payment Mode",
		"fieldname": "in_payment_mode",
		"fieldtype": "Data",
		"width": 100
	},
	{
		"label": "Inward",
		"fieldname": "in_amount",
		"fieldtype": "Currency",
		"width": 160
	},
	{
		"label": "Outward",
		"fieldname": "ex_amount",
		"fieldtype": "Currency",
		"width": 160
	},
	{
		"label": "Remarks",
		"fieldname": "in_remarks",
		"fieldtype": "Data",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]
	si_cash_type = frappe.db.sql("""select %s as inward_voucher_type, si.name as voucher_no,
					sip.amount as in_amount, si.remarks as in_remarks,
					sip.mode_of_payment as in_payment_mode
					from `tabSales Invoice` si join `tabSales Invoice Payment` sip
					on sip.parent = si.name
					where si.invoice_type = "Cash Invoice" and (sip.mode_of_payment ="Wire Transfer" or sip.mode_of_payment ="Credit Card" or sip.mode_of_payment ="Google Pay" or sip.mode_of_payment ="Cash") and si.posting_date 
					between %s and %s and si.docstatus = 1 and (si.status = 'Paid' or si.status = 'Credit Note Issued') """,
					('Sales Invoice',filters['cf_date'],filters['cf_date']),  as_dict = True)

	return_si = frappe.db.sql("""select %s as inward_voucher_type, si.name as voucher_no,
					sip.amount as in_amount, si.remarks as in_remarks,
					sip.mode_of_payment as in_payment_mode
					from `tabSales Invoice` si join `tabSales Invoice Payment` sip
					on sip.parent = si.name
					where si.invoice_type = "Cash Return" and (sip.mode_of_payment ="Wire Transfer" or sip.mode_of_payment ="Credit Card" or sip.mode_of_payment ="Google Pay" or sip.mode_of_payment ="Cash") and si.posting_date 
					between %s and %s and si.docstatus = 1 and si.is_return = 1 and si.status = 'Return'""",
					('Sales Invoice',filters['cf_date'],filters['cf_date']),  as_dict = True)

	pe_list_rc = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no,
					pe.paid_amount as in_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode
					from `tabPayment Entry` pe 
					where pe.payment_type = "Receive" and (pe.mode_of_payment ="Wire Transfer" or pe.mode_of_payment ="Credit Card" or pe.mode_of_payment ="Google Pay" or pe.mode_of_payment ="Cash" or pe.mode_of_payment = "Card Swiping") and pe.posting_date 
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	cust_pe_list_pay = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, 
					pe.paid_amount as ex_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode
					from `tabPayment Entry` pe 
					where pe.payment_type = "Pay" and pe.party_type = 'Customer' and (pe.mode_of_payment ="Wire Transfer" or pe.mode_of_payment ="Credit Card" or pe.mode_of_payment ="Google Pay" or pe.mode_of_payment ="Cash" or pe.mode_of_payment = "Card Swiping") and pe.posting_date  
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	common_pe_list_pay = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, 
					pe.paid_amount as ex_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode
					from `tabPayment Entry` pe 
					where pe.payment_type = "Pay" and (pe.party_type = 'Supplier' or pe.party_type = 'Employee') and (pe.mode_of_payment ="Cash" or pe.mode_of_payment = "Card Swiping") and pe.posting_date  
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	loan_disbursement_list = frappe.db.sql('''select %s as inward_voucher_type, ld.name as voucher_no, 
					ld.disbursed_amount as ex_amount,
					l.mode_of_payment as in_payment_mode
					from `tabLoan Disbursement` ld join `tabLoan` l
					on l.name = ld.against_loan
					where l.mode_of_payment ="Cash" and ld.disbursement_date  
					between %s and %s and ld.docstatus = 1''',
					('Loan Disbursement',filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	je_list = frappe.db.sql('''select  %s as inward_voucher_type, je.name as voucher_no, 
				je.total_debit as ex_amount, je.remark as in_remarks, 'Cash' as in_payment_mode
				from `tabJournal Entry` je
				where je.voucher_type = 'Cash Entry' and je.posting_date  between %s and %s 
				and je.docstatus = 1''',
				('Journal Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	data = si_cash_type + return_si + pe_list_rc + je_list + cust_pe_list_pay + common_pe_list_pay + loan_disbursement_list
	for i in data:
		if not 'in_amount' in i:
			i['in_amount'] = 0
		if not 'ex_amount' in i:
			i['ex_amount'] = 0
		if 'in_amount' in i and i['in_amount'] and i['in_amount']<0 :
			i['ex_amount']=abs(i['in_amount'])
			i['in_amount']=0

		if i['in_payment_mode']!='Cash':
			i['ex_amount']=i['in_amount']
	return data


def calculate_amount(entries,filters):
	total_sales = 0
	closing_cash = filters['cf_opening_balance'] if 'cf_opening_balance' in filters else 0
	
	total_sales = sum([entry['in_amount'] if 'in_amount' in entry else 0 for entry in entries if 'inward_voucher_type' in entry])
	
	closing_cash += sum([entry['in_amount'] if 'in_amount' in entry else 0 for entry in entries if ('inward_voucher_type' in entry and entry['in_payment_mode'] == 'Cash')]) - \
	sum([entry['ex_amount'] if 'ex_amount' in entry else 0 for entry in entries if ('inward_voucher_type' in entry and entry['in_payment_mode'] == 'Cash')])

	if frappe.db.exists('Daily Balance',{'date':filters['cf_date']}):
		frappe.db.set_value('Daily Balance',{'date':filters['cf_date']},'amount',closing_cash)
	else:
		frappe.get_doc({'doctype':'Daily Balance', 'date':filters['cf_date'],'amount':closing_cash}).insert()
	
	frappe.db.commit()
	
	return [{'in_payment_mode':frappe.bold('Closing Cash'),'ex_amount':closing_cash},{'in_payment_mode':frappe.bold('Total Sales'),'ex_amount':total_sales}]