# mpesa_b2c_integration

This app enables a B2C (Business-to-Customer) M-Pesa payout flow from the ERPNext Payment Entry form.

It is designed to be installed on Frappe Cloud and to trigger M-Pesa when a Payment Entry is created/submitted.

## Features
- M-Pesa Settings DocType with credentials stored securely
- Payment trigger from Payment Entry
- Access token generation
- B2C payment request to Safaricom
- Result and timeout callback endpoints
- Logs for requests and responses
- Manual button and automatic submit trigger

## Flow
1. Configure M-Pesa settings in ERPNext.
2. Create a Payment Entry with `payment_type = 'Pay'`.
3. ERPNext fetches the recipient mobile number from the customer/contact linked to the party.
4. A B2C request is sent to Safaricom.
5. Safaricom result is received via the callback URL.

## Important
- Default URL is the Safaricom sandbox.
- In production, update the base URL to the live M-Pesa API.
- This app assumes the payer is the business and the recipient is the customer.

## Installation
1. Install the app in your Frappe site.
2. Create a DocType called `MPesa Settings` using this app.
3. Fill in:
   - Consumer Key
   - Consumer Secret
   - Initiator Name
   - Security Credential
   - Shortcode
   - Result URL
   - Timeout URL
4. Submit a Payment Entry with `payment_type = 'Pay'` and `mode_of_payment = 'M-Pesa B2C'`.

## Callback URLs
Example:
- https://your-site.frappecloud.com/mpesa/b2c/result
- https://your-site.frappecloud.com/mpesa/b2c/timeout

## Notes
This is a payout flow (B2C). If your real requirement is a customer payment collection flow, use Safaricom STK Push instead.
