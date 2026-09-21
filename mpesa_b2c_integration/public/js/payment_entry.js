import frappe
import requests
from frappe.utils import now_datetime
from frappe.utils.password import get_decrypted_password

MPESA_BASE_URL = "https://sandbox.safaricom.co.ke"


def get_access_token():
    settings = frappe.get_single("MPesa Settings")
    if not settings.enabled:
        frappe.throw("M-Pesa B2C is disabled.")

    consumer_key = settings.consumer_key
    consumer_secret = get_decrypted_password("MPesa Settings", "MPesa Settings", "consumer_secret")

    if not consumer_key or not consumer_secret:
        frappe.throw("Consumer key or secret missing in M-Pesa Settings.")

    url = f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret), timeout=30)
    response.raise_for_status()

    data = response.json()
    access_token = data.get("access_token")
    if not access_token:
        frappe.throw("Unable to generate M-Pesa access token.")
    return access_token


def send_b2c_payment(payment_entry_name, phone_number, amount, remarks=None):
    payment_entry = frappe.get_doc("Payment Entry", payment_entry_name)
    settings = frappe.get_single("MPesa Settings")

    if not settings.enabled:
        frappe.throw("M-Pesa B2C is disabled.")

    if not phone_number:
        frappe.throw("Recipient mobile number is missing.")

    if amount <= 0:
        frappe.throw("Amount must be greater than zero.")

    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "InitiatorName": settings.initiator_name,
        "SecurityCredential": get_decrypted_password("MPesa Settings", "MPesa Settings", "security_credential"),
        "CommandID": "BusinessPayment",
        "Amount": int(float(amount)),
        "PartyA": settings.shortcode,
        "PartyB": str(phone_number).replace(" ", "").replace("-", ""),
        "Remarks": remarks or settings.remarks or "ERPNext B2C payment",
        "QueueTimeOutURL": settings.timeout_url,
        "ResultURL": settings.result_url,
        "Occasion": f"PE-{payment_entry.name}",
    }

    endpoint = f"{MPESA_BASE_URL}/mpesa/b2c/v1/paymentrequest"
    response = requests.post(endpoint, json=payload, headers=headers, timeout=30)

    if response.status_code >= 400:
        frappe.log_error(title="M-Pesa B2C Request Failed", message=response.text)
        frappe.throw(f"M-Pesa request failed: {response.text}")

    result = response.json()

    conversation_id = result.get("ConversationID") or result.get("OriginatorConversationID")
    frappe.get_doc(
        {
            "doctype": "MPesa B2C Log",
            "payment_entry": payment_entry.name,
            "request_id": conversation_id,
            "status": "Submitted",
            "request_payload": frappe.as_json(payload),
            "response_payload": frappe.as_json(result),
            "request_time": now_datetime(),
        }
    ).insert(ignore_permissions=True)

    payment_entry.db_set("mpesa_request_id", conversation_id)
    payment_entry.db_set("mpesa_status", "Submitted")

    return result
