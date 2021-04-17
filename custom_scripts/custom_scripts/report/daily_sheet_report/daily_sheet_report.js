// Copyright (c) 2016, C.R.I.O and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Sheet Report"] = {

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
			fieldname: "cf_date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			on_change:  function(){

				var date = frappe.query_report.get_filter_value('cf_date')
				frappe.db.exists("Daily Balance",`DB-${frappe.datetime.add_days(date, -1)}`)
				.then(r => {
					if(r){
					frappe.db.get_value("Daily Balance", {"date": frappe.datetime.add_days(date, -1)}, "amount", 
					(r1) => {
						frappe.query_report.set_filter_value('cf_opening_balance',r1.amount) });
					}else{
						frappe.query_report.set_filter_value('cf_opening_balance',0);
					}
						});
			},
			reqd: 1
		},
		{
			fieldname: "cf_opening_balance",
			label: __("Opening Balance"),
			fieldtype: "Currency",
			read_only: 1
		},
	]
};