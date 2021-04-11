// Copyright (c) 2016, C.R.I.O and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales person Incentive"] = {
	"filters": [
		{
			fieldname: "cf_company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "cf_from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1
		},
		{
			fieldname:"cf_to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "cf_sales_person",
			label: __("Sales Person"),
			fieldtype: "Link",
			options: "Sales Person",
		}
	]
};
