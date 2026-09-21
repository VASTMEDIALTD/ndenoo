import frappe
from frappe import _
from frappe.utils import now_datetime


@frappe.whitelist(allow_guest=True)
def result_url():
    data = frappe.local.form_dict
    frappe.log_error(title="M-Pesa B2C Result", message=str(data))

    # Example lookup pattern for the corresponding Payment Entry.
    # conversation_id = data.get("ConversationID")
    # payment_entry_name = frappe.db.get_value(
    #     "Payment Entry",
    #     {"mpesa_request_id": conversation_id},
    #     "name",
    # )
    # if payment_entry_name:
    #     frappe.db.set_value("Payment Entry", payment_entry_name, "mpesa_status", "Received")

    return "OK"


@frappe.whitelist(allow_guest=True)
def timeout_url():
    data = frappe.local.form_dict
    frappe.log_error(title="M-Pesa B2C Timeout", message=str(data))
    return "OK"
