# Copyright (c) 2021, C.R.I.O and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class CashDenomination(Document):
	def validate(self):
		self.total_amount = 0
		is_exist = frappe.db.get_value('Cash Denomination', {'date': self.date})
		if is_exist:
			if not self.name == is_exist:
				frappe.throw(_(f'Cash Denomination {is_exist} already exist for the selected date'))
		for row in self.cash_denominations_details:
			if row.total:
				self.total_amount += row.total
