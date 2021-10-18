frappe.ui.form.on("Sales Invoice Item",
{
	inches: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		if (d.inches) {
			frappe.model.set_value(cdt, cdn, 'qty', d.inches * 0.00694444);

		}
	}
});
