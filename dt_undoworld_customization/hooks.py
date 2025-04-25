app_name = "dt_undoworld_customization"
app_title = "DT-UndoWorld-Customization"
app_publisher = "DTPL"
app_description = "Minor customizations for UndoWorld Pvt Ltd"
app_email = "support@digitalistech.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dt_undoworld_customization/css/dt_undoworld_customization.css"
# app_include_js = "/assets/dt_undoworld_customization/js/dt_undoworld_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/dt_undoworld_customization/css/dt_undoworld_customization.css"
# web_include_js = "/assets/dt_undoworld_customization/js/dt_undoworld_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dt_undoworld_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Serial No" : "public/js/serial_no.js",
              "Stock Entry" : "public/js/stock_entry.js",
              "Work Order" : "public/js/work_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dt_undoworld_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dt_undoworld_customization.utils.jinja_methods",
# 	"filters": "dt_undoworld_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dt_undoworld_customization.install.before_install"
# after_install = "dt_undoworld_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dt_undoworld_customization.uninstall.before_uninstall"
# after_uninstall = "dt_undoworld_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dt_undoworld_customization.utils.before_app_install"
# after_app_install = "dt_undoworld_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dt_undoworld_customization.utils.before_app_uninstall"
# after_app_uninstall = "dt_undoworld_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dt_undoworld_customization.notifications.get_notification_config"

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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dt_undoworld_customization.tasks.all"
# 	],
# 	"daily": [
# 		"dt_undoworld_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"dt_undoworld_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dt_undoworld_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dt_undoworld_customization.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dt_undoworld_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.stock.doctype.delivery_note.delivery_note.make_sales_invoice": "dt_undoworld_customization.custom_scripts.custom_delivery_note.custom_make_sales_invoice"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dt_undoworld_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dt_undoworld_customization.utils.before_request"]
# after_request = ["dt_undoworld_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["dt_undoworld_customization.utils.before_job"]
# after_job = ["dt_undoworld_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dt_undoworld_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

doc_events = {
	"Stock Entry": {
		"before_validate": "dt_undoworld_customization.public.py.stock_entry.before_validate",
        "validate": "dt_undoworld_customization.public.py.stock_entry.validate",
        "before_cancel": "dt_undoworld_customization.public.py.stock_entry.before_cancel"
	},
    "BOM": {
            "before_validate": "dt_undoworld_customization.public.py.bom.before_validate",
            "validate": "dt_undoworld_customization.public.py.bom.validate"
        },
    "Serial and Batch Bundle": {
            "on_submit": "dt_undoworld_customization.public.py.s_and_b_bundle.on_submit"
        },
    "Delivery Note": {
            "on_submit": "dt_undoworld_customization.public.py.delivery_note.on_submit"
        },
    "Sales Invoice": {
            "before_submit": "dt_undoworld_customization.public.py.sales_invoice.before_submit"
        }
}

fixtures = [
    {"dt": "Custom Field",
     "filters": {'module':'DT-UndoWorld-Customization'}
        },
    {"dt": "Server Script",
     "filters": {'module':'DT-UndoWorld-Customization'}
        },
]

override_doctype_dashboards = {
	"Serial No": "dt_undoworld_customization.public.py.serial_no_dashboard.get_data"
}

auto_cancel_exempted_doctypes =['Stock Entry']


# override_methods = {
#     'hrms.payroll.doctype.payroll_entry.payroll_entry.PayrollEntry.make_accrual_jv_entry': 'dt_undoworld_customization.public.py.payroll.make_accrual_jv_entry',
# }


override_doctype_class = {
	"Payroll Entry": "dt_undoworld_customization.public.py.payroll.customPayrollEntry",
    "Stock Entry" : "dt_undoworld_customization.public.py.stock_entry.customStockEntry"
}