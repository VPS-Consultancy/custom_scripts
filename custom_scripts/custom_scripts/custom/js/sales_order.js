frappe.ui.form.on('Sales Order Item', {
	items_add: function(frm){
		frm.set_df_property('so_itemwise_rate_details', 'hidden', 1);
	},
  item_code: function (frm, cdt, cdn) {
    var d = locals[cdt][cdn]

    if(!d.item_code){
      frm.set_df_property('so_itemwise_rate_details', 'hidden', 1);
    }
    if(d.item_code){
      frm.set_df_property('so_itemwise_rate_details', 'hidden', 0);
      frappe.call({
        method: "custom_scripts.custom_scripts.custom.py.sales_order.fetch_rate_details",
        args: {
          item_code: d.item_code
        },
        freeze: true,
        callback: function (r) {
            if(r.message) {
                frm.set_value('so_itemwise_rate_details', r.message);
            }
            refresh_field('so_itemwise_rate_details');
        }
      })
    }
  }
});