# import frappe 
# @frappe.whitelist()
# def fetch_rate_details(item_code):
#     doc_count = 0
#     rate_details = []
#     so_details = frappe.get_all('Sales Invoice Item',['rate','parent'],{'item_code':item_code,'parenttype':'Sales Invoice', 'docstatus':1},order_by="modified")
#     for row in so_details[::-1]:
#         if frappe.db.get_value('Sales Invoice', row.parent,'docstatus') == 1:
#             so_doc = frappe.get_doc('Sales Invoice', row.parent)
#             rate_details.append(
#                 {
#                 'sales_invoice': row.parent,
#                 'date': so_doc.posting_date,
#                 'customer': so_doc.customer, 
#                 'rate': row.rate}
#             )
#             doc_count += 1
#         if doc_count == 5:
#             break
#     return rate_details

import frappe 

@frappe.whitelist()
def fetch_rate_details(item_code, customer):
    doc_count = 0
    rate_details = []

    so_details = frappe.get_all(
        'Sales Invoice Item',
        ['rate', 'parent'],
        {
            'item_code': item_code,
            'parenttype': 'Sales Invoice',
            'docstatus': 1
        },
        order_by="modified"
    )

    for row in so_details[::-1]:
        if frappe.db.get_value('Sales Invoice', row.parent, 'docstatus') == 1:
            so_doc = frappe.get_doc('Sales Invoice', row.parent)

            # Check if the customer matches the specified customer
            if so_doc.customer == customer:
                rate_details.append(
                    {
                        'sales_invoice': row.parent,
                        'date': so_doc.posting_date,
                        'customer': so_doc.customer, 
                        'rate': row.rate
                    }
                )
                doc_count += 1
            if doc_count == 5:
                break

    return rate_details
