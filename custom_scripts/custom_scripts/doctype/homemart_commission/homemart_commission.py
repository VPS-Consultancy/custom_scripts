# Copyright (c) 2023, C.R.I.O and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HomemartCommission(Document):
	def validate(self):
		total = 0
		for i in self.invoices:
			total += int(i.commison_amount)
		self.total = total

	def on_submit(self):
		for i in self.invoices:
			frappe.db.set_value('Sales Invoice',i.invoice, 'nhm_commission_status', 'Paid')
			frappe.db.commit()
	
	def on_cancel(self):
		for i in self.invoices:
			frappe.db.set_value('Sales Invoice',i.invoice, 'nhm_commission_status', 'Not Paid')
			frappe.db.commit()
