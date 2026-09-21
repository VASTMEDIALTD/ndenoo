frappe.ui.form.on('Payment Entry', {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.payment_type === 'Pay') {
            frm.add_custom_button(__('Send via M-Pesa'), function() {
                frappe.call({
                    method: 'mpesa_b2c_integration.payment_entry.trigger_b2c_from_payment_entry',
                    args: {
                        payment_entry_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('M-Pesa request queued successfully.'));
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    }
});
