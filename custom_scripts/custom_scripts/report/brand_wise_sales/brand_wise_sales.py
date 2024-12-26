# Copyright (c) 2024, C.R.I.O and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _
from frappe.query_builder import functions as fn
from frappe.utils import getdate
from frappe.query_builder.functions import Coalesce

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
			"amount": (item.amount or 0) + (item.cgst_amount or 0) + (item.sgst_amount or 0) + (item.igst_amount or 0),
			"indent": 1,
			"has_value": 1,
		})

	frappe.errprint(data)
	return columns, data


def get_columns():
	return [
		{"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Data", "width": 150},
		{"label": _("Brand"), "fieldname": "brand", "fieldtype": "Link", "options": "Brand", "width": 100},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 100},
	]


def get_item_info(filters):
	si = frappe.qb.DocType("Sales Invoice")
	sii = frappe.qb.DocType("Sales Invoice Item")
	item = frappe.qb.DocType("Item")
	
	# Check if fields exist in the table
	table_columns = frappe.db.get_table_columns("Sales Invoice Item")
	
	tax_fields = []
	if "cgst_amount" in table_columns:
		tax_fields.append(Coalesce(sii.cgst_amount, 0).as_("cgst_amount"))
   
	if "sgst_amount" in table_columns:
		tax_fields.append(Coalesce(sii.sgst_amount, 0).as_("sgst_amount"))
	
	if "igst_amount" in table_columns:
		tax_fields.append(Coalesce(sii.igst_amount, 0).as_("igst_amount"))
	
	# Build query with dynamic inclusion of tax fields
	query = (
		frappe.qb.from_(si)
		.join(sii).on(si.name == sii.parent)
		.left_join(item).on(sii.item_code == item.name)
		.select(
			item.item_group,
			item.brand,
			fn.Sum(sii.base_net_amount).as_("amount"),
			*tax_fields,  # Dynamically include only existing tax fields
		)
		.where(
			(si.docstatus == 1)
			& (si.posting_date >= filters.get("from_date"))
			& (si.posting_date <= filters.get("to_date"))
		)
	)
	
	# Add brand filter condition if 'brand' is provided in the filters
	if filters.get("brand"):
		query = query.where(item.brand == filters.get("brand"))
	
	query = query.groupby(item.item_group, item.brand)

	return query.run(as_dict=True)