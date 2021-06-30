from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt, nowdate, get_first_day, add_months, cstr, now_datetime, month_diff
from erpnext.hr.doctype.employee_advance.employee_advance import  EmployeeAdvance

class ERPNextEmployeeAdvance(EmployeeAdvance):
	def set_total_advance_paid(self):
		paid_amount = frappe.db.sql("""
			select ifnull(sum(debit), 0) as paid_amount
			from `tabGL Entry`
			where against_voucher_type = 'Employee Advance'
				and against_voucher = %s
				and party_type = 'Employee'
				and party = %s
		""", (self.name, self.employee), as_dict=1)[0].paid_amount

		return_amount = frappe.db.sql("""
			select ifnull(sum(credit), 0) as return_amount
			from `tabGL Entry`
			where against_voucher_type = 'Employee Advance'
				and voucher_type != 'Expense Claim'
				and against_voucher = %s
				and party_type = 'Employee'
				and party = %s
		""", (self.name, self.employee), as_dict=1)[0].return_amount

		if paid_amount != 0:
			paid_amount = flt(paid_amount) / flt(self.exchange_rate)
		if return_amount != 0:
			return_amount = flt(return_amount) / flt(self.exchange_rate)

		if flt(paid_amount) > self.advance_amount:
			frappe.throw(_("Row {0}# Paid Amount cannot be greater than requested advance amount"),
				EmployeeAdvanceOverPayment)

		if flt(return_amount) > self.paid_amount - self.claimed_amount:
			frappe.throw(_("Return amount cannot be greater unclaimed amount"))

		self.db_set("paid_amount", paid_amount)
		self.db_set("return_amount", return_amount)
		self.set_status()
		frappe.db.set_value("Employee Advance", self.name , "status", self.status)
		if self.repay_unclaimed_amount_from_salary == 1 and self.status == "Paid":
			payroll_date = get_first_day(add_months(nowdate(), 1))
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.employee_name = self.employee_name
			add_salary.company = self.company
			add_salary.salary_component = 'Employee Advance'
			add_salary.amount = self.paid_amount
			add_salary.ref_doctype = 'Employee Advance'
			add_salary.ref_docname = self.name
			add_salary.overwrite_salary_structure_amount = 1
			add_salary.save()
			add_salary.submit()
