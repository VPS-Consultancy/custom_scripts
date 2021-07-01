{% include 'erpnext/accounts/doctype/sales_invoice/sales_invoice.js' %};

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm){
        if(frm.doc.docstatus===1){
        this.frm.page.add_menu_item(__('Notify Customer'), function() { 
            frm.trigger('send_sms');});
        }
    },

    send_sms: function() {
    }
})  