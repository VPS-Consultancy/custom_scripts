# Copyright (c) 2013, C.R.I.O and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

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
		"width": 150
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
	{
		"label": "Party Type",
		"fieldname": "party_type",
		"fieldtype": "Data",
		"width": 100
	},
		{
		"label": "Party",
		"fieldname": "party",
		"fieldtype": "Dynamic Link",
		"options": "party_type",
		"width": 200
	},
	]
	return columns

def get_data(filters):
	data =[]
	si_cash_type = frappe.db.sql("""select %s as inward_voucher_type, si.name as voucher_no,
					sip.amount as in_amount, si.remarks as in_remarks,
					sip.mode_of_payment as in_payment_mode, si.customer as party, %s as party_type
					from `tabSales Invoice` si join `tabSales Invoice Payment` sip
					on sip.parent = si.name
					where si.invoice_type = "Cash Invoice" and (sip.mode_of_payment ="Wire Transfer" or sip.mode_of_payment ="Credit Card" or sip.mode_of_payment ="Google Pay" or sip.mode_of_payment ="Cash") and si.posting_date 
					between %s and %s and si.docstatus = 1 and (si.status = 'Paid' or si.status = 'Credit Note Issued') """,
					('Sales Invoice','Customer', filters['cf_date'],filters['cf_date']),  as_dict = True)

	return_si = frappe.db.sql("""select %s as inward_voucher_type, si.name as voucher_no,
					sip.amount as in_amount, si.remarks as in_remarks,
					sip.mode_of_payment as in_payment_mode, si.customer as party, %s as party_type
					from `tabSales Invoice` si join `tabSales Invoice Payment` sip
					on sip.parent = si.name
					where si.invoice_type = "Cash Return" and (sip.mode_of_payment ="Wire Transfer" or sip.mode_of_payment ="Credit Card" or sip.mode_of_payment ="Google Pay" or sip.mode_of_payment ="Cash") and si.posting_date 
					between %s and %s and si.docstatus = 1 and si.is_return = 1 and si.status = 'Return'""",
					('Sales Invoice','Customer',filters['cf_date'],filters['cf_date']),  as_dict = True)

	pe_list_rc = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no,
					pe.paid_amount as in_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode, pe.party_type, pe.party
					from `tabPayment Entry` pe 
					where pe.payment_type = "Receive" and (pe.mode_of_payment ="Wire Transfer" or pe.mode_of_payment ="Credit Card" or pe.mode_of_payment ="Google Pay" or pe.mode_of_payment ="Cash" or pe.mode_of_payment = "Card Swiping") and pe.posting_date 
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	cust_pe_list_pay = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, 
					pe.paid_amount as ex_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode, pe.party_type, pe.party
					from `tabPayment Entry` pe 
					where pe.payment_type = "Pay" and pe.party_type = 'Customer' and (pe.mode_of_payment ="Wire Transfer" or pe.mode_of_payment ="Credit Card" or pe.mode_of_payment ="Google Pay" or pe.mode_of_payment ="Cash" or pe.mode_of_payment = "Card Swiping") and pe.posting_date  
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)
	
	common_pe_list_pay = frappe.db.sql('''select %s as inward_voucher_type, pe.name as voucher_no, 
					pe.paid_amount as ex_amount, pe.remarks as in_remarks,
					pe.mode_of_payment as in_payment_mode, pe.party_type, pe.party
					from `tabPayment Entry` pe 
					where pe.payment_type = "Pay" and (pe.party_type = 'Supplier' or pe.party_type = 'Employee') and (pe.mode_of_payment ="Cash" or pe.mode_of_payment = "Card Swiping") and pe.posting_date  
					between %s and %s and pe.docstatus = 1''',
					('Payment Entry',filters['cf_date'],filters['cf_date']),  as_dict = True)

	loan_disbursement_list = frappe.db.sql('''select %s as inward_voucher_type, ld.name as voucher_no, 
					ld.disbursed_amount as ex_amount,
					l.mode_of_payment as in_payment_mode, ld.applicant_type as party_type, ld.applicant as party
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
		
		if i['inward_voucher_type'] == 'Journal Entry':
			jea_list = frappe.db.get_list('Journal Entry Account', {'parent': i['voucher_no']},['party_type', 'party'])
			for row in jea_list:
				if row['party_type']:
					i['party_type'] = row['party_type']
				if row['party']:
					i['party'] = row['party']

	data += calculate_amount(data,filters)
	return data


def calculate_amount(entries,filters):
	total = 0
	final_data  = []
	cl = abs(sum([entry['in_amount'] if 'in_amount' in entry and entry['in_payment_mode'] == 'Cash'  else 0 for entry in entries]) - sum([entry['ex_amount'] if 'ex_amount' in entry and entry['in_payment_mode'] == 'Cash'  else 0 for entry in entries]))
	total_in_amt = sum([entry['in_amount'] if 'in_amount' in entry else 0 for entry in entries])
	total_ex_amt = sum([entry['ex_amount'] if 'ex_amount' in entry else 0 for entry in entries])
	opening = filters['cf_opening_balance'] if 'cf_opening_balance' in filters else 0
	total = opening + total_in_amt
	final_data += [{'in_amount':total_in_amt, 'ex_amount': total_ex_amt}, {'in_payment_mode':frappe.bold('Opening'), 'in_amount':opening}, {'in_payment_mode':frappe.bold('Total'), 'in_amount': total, 'ex_amount': total_ex_amt},
	{'in_payment_mode':frappe.bold('Less Expenses'), 'in_amount': -total_ex_amt},
	{'in_payment_mode':frappe.bold('Closing Cash'), 'in_amount': total-total_ex_amt}
	]

	is_denomination_exist = frappe.db.get_value('Cash Denomination', {'date': filters['cf_date'], 'docstatus': 1})
	if is_denomination_exist:
		closing_cash = frappe.db.get_value('Cash Denomination', is_denomination_exist, 'total_amount')
		denomination_list = frappe.get_list('Cash Denominations Details', {'parent': is_denomination_exist}, ['denomination','count','total'])
		ordered_list = [['2000', 0, 0], ['500', 0, 0], ['200', 0, 0], ['100', 0, 0], ['50', 0, 0], ['20', 0, 0], ['10', 0, 0]]
		for row in denomination_list[::-1]:
			for row1 in ordered_list:
				if row.get('denomination') == row1[0]:
					row1[1] = row.get('count') if row.count else 0
					row1[2] = row.get('total') if row.total else 0
		if closing_cash:
			final_data += [{'in_payment_mode':frappe.bold('Difference'), 'in_amount': (total-total_ex_amt) - (closing_cash)}]
		final_data += [{'voucher_no':'', 'in_payment_mode':'', 'in_amount':''}]
		for row in ordered_list:
			final_data += [{'voucher_no':frappe.bold(row[0]), 'in_payment_mode':row[1], 'in_amount':row[2]}]

		final_data += [{'voucher_no':'', 'in_payment_mode':'', 'in_amount':closing_cash}]
		if closing_cash:
			if frappe.db.exists('Daily Summary Balance',{'date':filters['cf_date']}):
				frappe.db.set_value('Daily Summary Balance',{'date':filters['cf_date']},'amount',closing_cash)
			else:
				frappe.get_doc({'doctype':'Daily Summary Balance', 'date':filters['cf_date'],'amount':closing_cash}).insert()
			final_data += [
			{'inward_voucher_type':frappe.bold('**Closing Cash**'), 'voucher_no': frappe.bold(closing_cash)},
			{'inward_voucher_type':frappe.bold('**Total Sales** '), 'voucher_no': frappe.bold(total_in_amt)}]
	
	frappe.db.commit()
	
	return final_data