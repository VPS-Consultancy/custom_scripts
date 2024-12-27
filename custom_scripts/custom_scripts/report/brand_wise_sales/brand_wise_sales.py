# Copyright (c) 2024, C.R.I.O and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _
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
    # Prepare dynamic tax field sums based on table columns
    table_columns = frappe.db.get_table_columns("Sales Invoice Item")
    tax_fields = []
    if "cgst_amount" in table_columns:
        tax_fields.append("SUM(COALESCE(sii.cgst_amount, 0)) AS cgst_amount")
    if "sgst_amount" in table_columns:
        tax_fields.append("SUM(COALESCE(sii.sgst_amount, 0)) AS sgst_amount")
    if "igst_amount" in table_columns:
        tax_fields.append("SUM(COALESCE(sii.igst_amount, 0)) AS igst_amount")

    # Convert tax fields into a string for SQL query
    tax_fields_sql = ", ".join(tax_fields) if tax_fields else ""

    # Base query with dynamic tax fields
    query = f"""
        SELECT 
            item.item_group,
            item.brand,
            SUM(sii.base_net_amount) AS amount
            {f",{tax_fields_sql}" if tax_fields_sql else ""}
        FROM 
            `tabSales Invoice` AS si
        INNER JOIN 
            `tabSales Invoice Item` AS sii ON si.name = sii.parent
        LEFT JOIN 
            `tabItem` AS item ON sii.item_code = item.name
        WHERE 
            si.docstatus = 1
            AND si.posting_date >= %(from_date)s
            AND si.posting_date <= %(to_date)s
    """

    # Add brand filter condition if provided
    if filters.get("brand"):
        query += " AND item.brand = %(brand)s"

    # Group by item group and brand
    query += """
        GROUP BY 
            item.item_group, item.brand
    """

    # Execute the query and fetch results

    return frappe.db.sql(query, filters, as_dict=True)
