app_name = "mpesa_b2c_integration"
app_title = "MPesa B2C Integration"
app_publisher = "VASTMEDIALTD"
app_description = "M-Pesa B2C integration for ERPNext / Frappe Cloud"
app_email = "support@vastmedia.co.ke"
app_license = "mit"

required_apps = ["frappe", "erpnext"]

doctype_js = {
    "Payment Entry": ["public/js/payment_entry.js"],
}

website_route_rules = [
    {"from_route": "/mpesa/b2c/result", "to_route": "mpesa_b2c_integration.api.result_url"},
    {"from_route": "/mpesa/b2c/timeout", "to_route": "mpesa_b2c_integration.api.timeout_url"},
]

# Trigger automatically when a Payment Entry is submitted.
def on_submit(doc, method):
    if doc.doctype == "Payment Entry" and doc.payment_type == "Pay":
        from mpesa_b2c_integration.payment_entry import trigger_b2c_from_payment_entry
        if doc.mode_of_payment == "M-Pesa B2C":
            frappe.enqueue(
                "mpesa_b2c_integration.payment_entry.trigger_b2c_from_payment_entry",
                payment_entry_name=doc.name,
                queue="short",
                timeout=300,
            )


# Import frappe here only for enqueue usage.
import frappe
