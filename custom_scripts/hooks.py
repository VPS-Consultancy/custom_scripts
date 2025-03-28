# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "custom_scripts"
app_title = "Custom Scripts"
app_publisher = "C.R.I.O"
app_description = "For custom scripts"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "criogroups@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/custom_scripts/css/custom_scripts.css"
# app_include_js = "/assets/custom_scripts/js/custom_scripts.js"

# include js, css files in header of web template
# web_include_css = "/assets/custom_scripts/css/custom_scripts.css"
# web_include_js = "/assets/custom_scripts/js/custom_scripts.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "custom_scripts/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Sales Invoice" : "custom_scripts/custom/js/sales_invoice.js",
	"Sales Order" : "custom_scripts/custom/js/sales_order.js",
	"Purchase Order" : "custom_scripts/custom/js/purchase_order.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "custom_scripts.install.before_install"
# after_install = "custom_scripts.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "custom_scripts.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	#"Employee Advance": "custom_scripts.custom_scripts.custom.auto_additional_salary.ERPNextEmployeeAdvance",
	"POS Invoice Merge Log": "custom_scripts.custom_scripts.custom.sales_invoice.ERPNextPOSInvoiceMergeLog",
	"NHMCommision": "custom_scripts.custom_scripts.doctype.nhm_commission.NHMCommision"
}
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
	"Journal Entry":{
		"on_submit": "custom_scripts.custom_scripts.custom.journal_entry_custom.make_nhm_paid"
	},
	"Payment Entry":{
		"on_submit":"custom_scripts.custom_scripts.custom.py.payment_entry.on_submit",
		"on_cancel":"custom_scripts.custom_scripts.custom.py.payment_entry.on_cancel",
	},
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"custom_scripts.tasks.all"
# 	],
# 	"daily": [
# 		"custom_scripts.tasks.daily"
# 	],
# 	"hourly": [
# 		"custom_scripts.tasks.hourly"
# 	],
# 	"weekly": [
# 		"custom_scripts.tasks.weekly"
# 	]
# 	"monthly": [
# 		"custom_scripts.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "custom_scripts.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "custom_scripts.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "custom_scripts.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

cors = ["*"]
