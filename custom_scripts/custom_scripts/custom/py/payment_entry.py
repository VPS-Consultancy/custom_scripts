import frappe
def on_submit(doc,action):
    employee_advance_automation = frappe.db.get_single_value("Nirmala Settings", "automate_additional_salary_from_payment_entry")

    if employee_advance_automation == 1:
        for i in doc.references:
            if(i.reference_doctype=='Employee Advance'):
                advance_doc=frappe.get_doc('Employee Advance',i.reference_name)
                if advance_doc.repay_unclaimed_amount_from_salary == 1:
                    additional_salary_doc=frappe.new_doc('Additional Salary')
                    additional_salary_doc.employee = doc.party
                    additional_salary_doc.salary_component = 'Employee Advance'
                    additional_salary_doc.payroll_date=doc.posting_date
                    additional_salary_doc.amount=i.allocated_amount
                    additional_salary_doc.ref_doctype='Employee Advance'
                    additional_salary_doc.ref_docname=i.reference_name
                    additional_salary_doc.insert()
                    additional_salary_doc.submit()
                    frappe.db.commit()

def on_cancel(doc,action):
    employee_advance_automation = frappe.db.get_single_value("Nirmala Settings", "automate_additional_salary_from_payment_entry")

    if employee_advance_automation == 1:
        for i in doc.references:
            if(i.reference_doctype=='Employee Advance'):
                advance_doc=frappe.get_doc('Employee Advance',i.reference_name)
                if advance_doc.repay_unclaimed_amount_from_salary == 1:
                    for add_sal in frappe.get_all('Additional Salary',{'ref_docname':i.reference_name}):
                        add_doc = frappe.get_doc('Additional Salary',add_sal.name)
                        if add_doc.docstatus == 1:
                            add_doc.cancel()

                    frappe.db.commit()