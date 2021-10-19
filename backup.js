frappe.ui.form.on("Sales Invoice Item",
{
	inches: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		if (d.inches) {
		    if(d.inches>0 && d.inches<=3){
					frappe.model.set_value(cdt, cdn, 'qty', d.inches * 0.00694444);
				}
				else{
					const object = {1: [1,3], 6:[3,6], 9:[6,9], 12:[9,12],
					16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
					72:[60,72], 84:[72, 84], 96:[84, 96]
					};
					for (const [key, value] of Object.entries(object)) {
						if(d.inches>value[0] && d.inches<=value[1]){
							frappe.model.set_value(cdt, cdn, 'qty',key * 0.00694444);
						}
		
					}
				}
		}
	}
});
