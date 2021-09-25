frappe.ui.form.on("Sales Invoice", {
  refresh: function (frm) {
    if (frm.doc.docstatus == 1) {
      frm.add_custom_button("Notify Customer", function () {
        frm.trigger("notify_customer");
      });
    }
  },

  on_submit: function (frm) {
    frm.trigger("notify_customer");
  },
  notify_customer: function (frm) {
    frappe.call({
      method: "custom_scripts.custom_scripts.custom.sales_invoice.send_sms",
      args: {
        customer: frm.doc.customer,
        invoice_no: frm.doc.name,
        inv_date: frm.doc.posting_date,
        amount: frm.doc.rounded_total,
      },
      freeze: true,
      callback: function (r) {
        if (r.message) {
          frappe.show_alert({
            message: __("Message sent successfully"),
            indicator: "green",
          });
        } else {
          frappe.show_alert({
            message: __("Message sending failed"),
            indicator: "red",
          });
        }
      },
    });
  },
});
