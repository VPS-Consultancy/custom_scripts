import frappe
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def custom_login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()

        frappe.response["message"] = "Logged In"
        frappe.response["full_name"] = frappe.session.user
        frappe.response["sid"] = frappe.session.sid
        frappe.response["home_page"] = "/app"
    except frappe.AuthenticationError:
        frappe.response["message"] = "Invalid username or password"
        frappe.response["error"] = True
    except Exception as e:
        frappe.response["message"] = "An error occurred"
        frappe.response["error"] = str(e)

    return frappe.response
