
import frappe
from frappe.model.mapper import get_mapped_doc

from frappe.model.document import Document


def make_nhm_paid(doc,method):
    if doc.nhm_commision:
        for i in doc.accounts:
            if i.party_type == "Sales Partner":
                frappe.db.set_value("NHM Commision",doc.nhm_commision,{'payment_status':"Paid","journal_entry":doc.name})
                nhm_doc = frappe.db.sql(f""" select 
                                                nhm.name,
                                                nhmi.invoice as invoice
                                            from 
                                             `tabNHM Commision` nhm 
                                              left join `tabNHM Commision Item` nhmi on nhmi.parent = nhm.name
                                            where 
                                                nhm.name = '{doc.nhm_commision}'
                                         """,as_dict=1)
                frappe.db.set_value("Sales Invoice",nhm_doc[0]['invoice'],{'nhm_commission_status':"Paid"})

                
