import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("Sales Invoice"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 150,
        },
        {
            "fieldname": "posting_date",
            "label": _("Invoice Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "payment_date",
            "label": _("Payment Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "grand_total",
            "label": _("Grand Total"),
            "fieldtype": "Currency"
        },
        {
            "fieldname": "commission_amount",
            "label": _("Commission Amount"),
            "fieldtype": "Currency"
        }
    ]
    return columns


def get_data(filters):
    return frappe.db.sql("""
        SELECT
            `tabSales Invoice`.name,
            `tabSales Invoice`.posting_date,
            `tabPayment Entry`.posting_date AS payment_date,
            `tabSales Invoice`.grand_total,
            (`tabSales Invoice`.grand_total * 0.0075) AS commission_amount
        FROM
            `tabSales Invoice`
        JOIN
            `tabPayment Entry Reference`
        ON
            `tabPayment Entry Reference`.reference_name = `tabSales Invoice`.name
            AND `tabPayment Entry Reference`.reference_doctype = 'Sales Invoice'
            AND `tabPayment Entry Reference`.parenttype = 'Payment Entry'
        JOIN
            `tabPayment Entry`
        ON
            `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
            AND `tabPayment Entry`.docstatus = 1
            AND DATEDIFF(IFNULL(`tabPayment Entry`.posting_date, NOW()), `tabSales Invoice`.posting_date) <= 60
        WHERE
            `tabSales Invoice`.docstatus = 1
            AND `tabSales Invoice`.posting_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY
            `tabSales Invoice`.posting_date ASC
    """, filters, as_dict=True)
