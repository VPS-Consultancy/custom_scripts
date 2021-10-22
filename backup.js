frappe.ui.form.on("Sales Invoice Item",
{
    height: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		var inches = 0;
		if (d.height) {
			const object = {3: [0,3], 6:[3,6], 9:[6,9], 12:[9,12],
			16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
			72:[60,72], 84:[72, 84], 96:[84, 96]
			};
			for (const [key, value] of Object.entries(object)) {
				if(d.height>value[0] && d.height<=value[1]){
					if (d.inches!==0)
					{
						if(d.weight!==0){
							for (const [key1, value1] of Object.entries(object)) {
								if(d.weight>value1[0] && d.weight<=value1[1]){
									inches = key * key1;
								}
				
							}
						}
					}
					else{
						inches = key;
					}
				}

			}
			frappe.model.set_value(cdt, cdn, 'inches', inches);
			frappe.model.set_value(cdt, cdn, 'qty', inches * 0.00694444);
			
	}
	},
	weight: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		var inches = 0;
		if (d.weight) {
			const object = {3: [0,3], 6:[3,6], 9:[6,9], 12:[9,12],
			16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
			72:[60,72], 84:[72, 84], 96:[84, 96]
			};
			for (const [key, value] of Object.entries(object)) {
				if(d.weight>value[0] && d.weight<=value[1]){
					if (d.inches!==0)
					{
						if(d.height!==0){
							for (const [key1, value1] of Object.entries(object)) {
								if(d.height>value1[0] && d.height<=value1[1]){
									inches = key * key1;
								}
				
							}
						}
					}
					else{
						inches = key;
					}
				}

			}
			frappe.model.set_value(cdt, cdn, 'inches', inches);
			frappe.model.set_value(cdt, cdn, 'qty', inches * 0.00694444);
	}
	}
});
