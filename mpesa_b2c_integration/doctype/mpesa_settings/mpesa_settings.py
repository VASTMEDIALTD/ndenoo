import frappe
from frappe.model.document import Document
from frappe.utils.password import get_decrypted_password


class MPesaSettings(Document):
    pass


@frappe.whitelist()
def get_settings():
    doc = frappe.get_single("MPesa Settings")
    if not doc.enabled:
        frappe.throw("M-Pesa B2C is disabled.")

    return {
        "consumer_key": doc.consumer_key,
        "consumer_secret": get_decrypted_password("MPesa Settings", "MPesa Settings", "consumer_secret"),
        "initiator_name": doc.initiator_name,
        "security_credential": get_decrypted_password("MPesa Settings", "MPesa Settings", "security_credential"),
        "shortcode": doc.shortcode,
        "result_url": doc.result_url,
        "timeout_url": doc.timeout_url,
        "remarks": doc.remarks or "ERPNext B2C payment",
    }
