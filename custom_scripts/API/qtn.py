import frappe
from frappe.model.document import Document
from frappe.utils import get_site_url,today, add_days
from frappe.utils import flt

@frappe.whitelist(allow_guest=True)
def get_customers():
    items=frappe.db.get_all(
        "Customer",
        fields=[
            "customer_name"
        ]
    )
    return items

@frappe.whitelist(allow_guest=True)
def get_item_details():
    items = frappe.db.get_all(
        "Item", 
        fields=[
            "item_code",
            "item_name",
            "item_group",
            "image",
            "barcode"
        ],
    )

    for item in items:
        item_price = frappe.db.get_value(
            "Item Price", 
            {"item_code": item["item_code"], "selling": 1},  # Fetching selling price
            "price_list_rate"
        )

        frappe.logger().info(f"Item: {item['item_code']}, Price List Rate: {item_price}") 

        item["price_list_rate"] = item_price if item_price else 0  

    return items

@frappe.whitelist(allow_guest=True)
def get_salesperson():
    items = frappe.db.get_all(
        "Sales Person", 
        filters={"enabled": 1},  # Filter only enabled salespersons
        fields=["sales_person_name"]
    )
    return items


# @frappe.whitelist(allow_guest=True)
# def get_quotation_details():
#     quotation = frappe.db.get_all(
#         "Quotation", 
#         fields=[
#             "quotation_to", 
#             "naming_series",
#             "transaction_date",
#             "status",
#             "quotation_to",
#             "order_type",
#             "currency",
#             "company",
#             "conversion_rate",
#             "selling_price_list",
#             "price_list_currency",
#             "plc_conversion_rate",
#         ],
#     )

#     for quotations in quotation:
#         quotation_items = frappe.db.get_all(
#             "Quotation Item",
#             filters={"parent": quotations["name"]}, 
#             fields=["item_name", "qty","uom","conversion_factor"]
#         )
#         quotations["items"] = quotation_items 

#     return quotation

@frappe.whitelist(allow_guest=True)
def get_quotation_details():
    quotations = frappe.db.get_all(
        "Quotation", 
        fields=[
            "name",
            "quotation_to", 
            "naming_series",
            "party_name",
            "customer_name",
            "transaction_date",
            "valid_till",
            "contact_mobile",
            "status",
            "sales_person",
            "order_type",
            "currency",
            "company",
            "conversion_rate",
            "selling_price_list",
            "price_list_currency",
            "plc_conversion_rate",
        ],
    )

    for quotation in quotations:
        quotation_items = frappe.db.get_all(
            "Quotation Item",
            filters={"parent": quotation["name"]},  # Use correct reference
            fields=["item_name", "qty", "uom", "price_list_rate", "rate", "amount", "image"]
        )
        quotation["items"] = quotation_items  # Attach items to each quotation

    return quotations

