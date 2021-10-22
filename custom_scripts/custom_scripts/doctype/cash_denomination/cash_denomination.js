// Copyright (c) 2021, C.R.I.O and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Denomination', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Cash Denominations Details', {
	count: function(frm, cdt, cdn){
		let d = locals[cdt][cdn];
		if(d.count && d.denomination){
			frappe.model.set_value(cdt, cdn, 'total', flt(d.denomination) * d.count);
		}
	},
	denomination: function(frm, cdt, cdn){
		let d = locals[cdt][cdn];
		if(d.count && d.denomination){
			frappe.model.set_value(cdt, cdn, 'total', flt(d.denomination) * d.count);
		}
	}
});
