frappe.ui.form.on("Sales Invoice Item",
{
    no_of_pieces: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		var inches = 0;
		if (d.no_of_pieces) {
			frappe.model.set_value(cdt, cdn, 'qty', d.inches * 0.00694444 * d.no_of_pieces);
	}
	},
    height: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		var inches = 0;
		if (d.height) {
		    if(d.item_group == 'Regular Moving Glass')
		    {
		    const object = {3: [0,3], 6:[3,6], 12:[6,12], 15:[12,15],
			18:[15,18], 24:[18,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
			72:[60,72], 84:[72, 84], 96:[84, 96]
			};
		    }
		    if(d.item_group == 'Non-Regular Moving Glass'){
			const object = {12:[0,12], 18:[12,18], 24:[18,24], 36:[24,36], 48:[36,48], 60:[48,60], 72:[60,72]};
		    }
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
			frappe.model.set_value(cdt, cdn, 'qty', inches * 0.00694444 * d.no_of_pieces);
			
	}
	},
	weight: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		var inches = 0;
		if (d.weight) {
			if(d.item_group == 'Regular Moving Glass')
		    {
		    const object = {3: [0,3], 6:[3,6], 12:[6,12], 15:[12,15],
			18:[15,18], 24:[18,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
			72:[60,72], 84:[72, 84], 96:[84, 96]
			};
		    }
		    if(d.item_group == 'Non-Regular Moving Glass'){
			const object = {12:[0,12], 18:[12,18], 24:[18,24], 36:[24,36], 48:[36,48], 60:[48,60], 72:[60,72]};
		    }
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
			frappe.model.set_value(cdt, cdn, 'qty', inches * 0.00694444 * d.no_of_pieces);
	}
	}
});
