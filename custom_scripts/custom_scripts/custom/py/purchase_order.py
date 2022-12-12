import frappe

@frappe.whitelist()
def fetch_rate_details(item_code):
    doc_count = 0
    rate_details = []
    po_details = frappe.get_all('Purchase Order Item',['rate','parent'],{'item_code':item_code,'parenttype':'Purchase Order'},order_by="modified")
    for row in po_details[::-1]:
        if frappe.db.get_value('Purchase Order', row.parent,'docstatus') == 1:
            po_doc = frappe.get_doc('Purchase Order', row.parent)
            rate_details.append(
                {
                'purchase_order': row.parent,
                'date': po_doc.transaction_date,
                'supplier': po_doc.supplier, 
                'rate': row.rate}
            )
            doc_count += 1
        if doc_count == 5:
            break
    return rate_details