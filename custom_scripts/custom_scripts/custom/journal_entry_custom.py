
import frappe
from frappe.model.mapper import get_mapped_doc

from frappe.model.document import Document


def make_nhm_paid(doc,method):
    if doc.homemart_commission:
        for i in doc.accounts:
            if i.party_type == "Sales Partner":
                frappe.db.set_value("Homemart Commission",doc.homemart_commission,{'payment_status':"Paid","journal_entry":doc.name})
                nhm_doc = frappe.db.sql(f""" select 
                                                nhm.name,
                                                nhmi.invoice as invoice
                                            from 
                                             `tabHomemart Commission` nhm 
                                              left join `tabHomemart Commission Item` nhmi on nhmi.parent = nhm.name
                                            where 
                                                nhm.name = '{doc.homemart_commission}'
                                         """,as_dict=1)
                if nhm_doc:
                    for j in nhm_doc:
                        frappe.db.set_value("Sales Invoice",j['invoice'],{'nhm_commission_status':"Paid"})

                
