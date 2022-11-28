// Copyright (c) 2022, C.R.I.O and contributors
// For license information, please see license.txt

frappe.ui.form.on('NHM Commision', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('NHM Commision Item', {
    commison_amount:function(frm,cdt,cdn) {
		// your code here
         var blance=0
          frm.doc.table_3.forEach(function(d){
        		    blance += d.commison_amount
          })
          cur_frm.set_value('total',blance)
          cur_frm.refresh_field('total')
	
		
	},
	table_3_remove:function(frm,cdt,cdn){
	             var blance=0
          frm.doc.table_3.forEach(function(d){
        		    blance += d.commison_amount
          })
          cur_frm.set_value('total',blance)
          cur_frm.refresh_field('total')
	    
	}
})