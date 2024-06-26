// Copyright (c) 2023, C.R.I.O and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Commission Eligibility"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.now_date(), -30)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date()
        }
    ]
};
