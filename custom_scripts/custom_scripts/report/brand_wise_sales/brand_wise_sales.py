# Copyright (c) 2024, C.R.I.O and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _
from frappe.query_builder import functions as fn
from frappe.utils import getdate

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	items = get_item_info(filters)

	data = []
	item_group_map = {}
	for item in items:
		group = item.item_group
		if group not in item_group_map:
			data.append({
				"item_group": group,
				"indent": 0,
				"has_value": 0,
			})
			item_group_map[group] = True
		data.append({
			"brand": item.brand,
			"amount": item.amount,
			"indent": 1,
			"has_value": 1,
		})

	return columns, data


def get_columns():
	return [
		{"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Data", "width": 150},
		{"label": _("Brand"), "fieldname": "brand", "fieldtype": "Link", "options": "Brand", "width": 100},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 100},
	]


def get_item_info(filters):
    item = frappe.qb.DocType("Item")
    sales_invoice_item = frappe.qb.DocType("Sales Invoice Item")
    sales_invoice = frappe.qb.DocType("Sales Invoice")
    
    query = (
        frappe.qb.from_(item)
        .join(sales_invoice_item).on(sales_invoice_item.item_code == item.name)
        .join(sales_invoice).on(sales_invoice_item.parent == sales_invoice.name)
        .select(
            item.item_group,
            item.brand,
            fn.Sum(sales_invoice_item.amount).as_("amount")
        )
        .where(
            (sales_invoice.docstatus == 1)  # Only include submitted invoices
            & (sales_invoice.posting_date >= filters.get("from_date"))
            & (sales_invoice.posting_date <= filters.get("to_date"))
        )
    )
    
    # Add brand filter condition if 'brand' is provided in the filters
    if filters.get("brand"):
        query = query.where(item.brand == filters.get("brand"))

    query = query.groupby(item.item_group, item.brand)  # Group by item group and brand

    return query.run(as_dict=True)