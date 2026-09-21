import frappe
from frappe.utils import now_datetime


@frappe.whitelist()
def trigger_b2c_from_payment_entry(payment_entry_name):
    pe = frappe.get_doc("Payment Entry", payment_entry_name)

    if pe.docstatus != 1:
        frappe.throw("Payment Entry must be submitted before sending to M-Pesa.")

    if pe.payment_type != "Pay":
        frappe.throw("M-Pesa B2C is for payout Payment Entries only. Use payment_type='Pay'.")

    if not pe.party:
        frappe.throw("Party is missing in Payment Entry.")

    phone_number = get_customer_phone(pe.party)
    if not phone_number:
        frappe.throw("Customer phone number not found for the linked party.")

    amount = pe.paid_amount or pe.received_amount
    if not amount:
        frappe.throw("Payment Entry amount is missing.")

    return enqueue_b2c_payment(
        payment_entry_name=pe.name,
        phone_number=phone_number,
        amount=amount,
        remarks=f"Payment Entry {pe.name}",
    )


def get_customer_phone(party):
    customer = frappe.db.get_value(
        "Customer",
        {"name": party},
        ["mobile_no", "phone"],
        as_dict=True,
    )
    if customer and (customer.mobile_no or customer.phone):
        return normalize_phone(customer.mobile_no or customer.phone)

    link = frappe.db.get_value(
        "Dynamic Link",
        {"link_name": party, "link_doctype": "Customer"},
        "parent",
    )
    if link:
        contact = frappe.db.get_value("Contact", link, ["mobile_no", "phone"], as_dict=True)
        if contact and (contact.mobile_no or contact.phone):
            return normalize_phone(contact.mobile_no or contact.phone)

    return None


def normalize_phone(phone):
    if not phone:
        return None
    return str(phone).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


def enqueue_b2c_payment(payment_entry_name, phone_number, amount, remarks=None):
    frappe.enqueue(
        "mpesa_b2c_integration.utils.send_b2c_payment",
        queue="short",
        job_name=f"mpesa_b2c_{payment_entry_name}",
        payment_entry_name=payment_entry_name,
        phone_number=phone_number,
        amount=amount,
        remarks=remarks,
        timeout=300,
    )
    return {"status": "queued", "payment_entry": payment_entry_name}
