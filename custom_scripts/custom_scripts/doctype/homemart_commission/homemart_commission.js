// Copyright (c) 2023, C.R.I.O and contributors
// For license information, please see license.txt

frappe.ui.form.on('Homemart Commission', {
	refresh: function(frm) {
    frm.set_query("invoice", "invoices", function () {
			return {
				filters: {
					nhm_commission_status: ["!=","Paid"],
          is_return: ["!=",1]
				},
			};
		});

	}
});
frappe.ui.form.on('Homemart Commission Item', {
    commison_amount:function(frm,cdt,cdn) {
		// your code here
         var blance=0
          frm.doc.invoices.forEach(function(d){
        		    blance += d.commison_amount
          })
          cur_frm.set_value('total',blance)
          cur_frm.refresh_field('total')
	
		
	},
	invoices_remove:function(frm,cdt,cdn){
	             var blance=0
          frm.doc.invoices.forEach(function(d){
        		    blance += d.commison_amount
          })
          cur_frm.set_value('total',blance)
          cur_frm.refresh_field('total')
	    
	}
})