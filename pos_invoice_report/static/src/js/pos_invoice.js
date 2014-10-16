openerp.pos_invoice_report = function (instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    var module=instance.point_of_sale
    console.log("cfjdfjhfhfh",module)
    module.PosModel.prototype.models.push(
//    		{
//        model:  'stock.warehouse',
//        fields: ['name', 'id','qr_code_ids'],
//        domain:  null,
//        loaded: function(self, stock){
//            console.log("stock",stock)
//            self.warehouse_list = stock
//        },
//    },
    {
		model:  'qr.code',
		fields: ['nit_code_comapny', 'id'],
		domain:  null,
		loaded: function(self, qr){
		self.qr_list = qr
        }
    },
    {
        model:  'pos.session',
        fields: ['id', 'journal_ids','name','qr_code_ids','user_id','config_id','start_at','stop_at','sequence_number','login_number'],
        domain: function(self){ return [['state','=','opened'],['user_id','=',self.session.uid]]; },
        loaded: function(self,pos_sessions){
            self.pos_session = pos_sessions[0]; 
            session_qrs = []
            for(qr in self.pos_session.qr_code_ids){
                _.each(self.qr_list, function(qrs){
                    if(self.pos_session.qr_code_ids[qr] == qrs.id){
                        session_qrs.push(qrs)
                    }
                });
            }
            self.session_qrs = session_qrs
            var orders = self.db.get_orders();
            for (var i = 0; i < orders.length; i++) {
                self.pos_session.sequence_number = Math.max(self.pos_session.sequence_number, orders[i].data.sequence_number+1);
            }
        },
    });

    module.Order = module.Order.extend({
        // exports a JSON for receipt printing
        exportAsJSON: function() {
            var orderLines, paymentLines;
            orderLines = [];
            (this.get('orderLines')).each(_.bind( function(item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            paymentLines = [];
            (this.get('paymentLines')).each(_.bind( function(item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            this.partner_id = 0
            if(this.attributes.partner_id){
                for(partner in this.pos.partner_list){
                    if(this.pos.partner_list[partner].name == this.attributes.partner_id){
                        this.partner_id = this.pos.partner_list[partner].id
                    }
             }
            }
            return {
                name: this.getName(),
                pflag:this.getFlag(),
                parcel: this.getParcel(),
                amount_paid: this.getPaidTotal(),
                amount_total: this.getTotal(),
                amount_tax: this.getTax(),
                amount_return: this.getChange(),
                lines: orderLines,
                statement_ids: paymentLines,
                pos_session_id: this.pos.pos_session.id,
                partner_id: this.get_client() ? this.get_client().id : null,
                phone: this.getphone(),
                pricelist_id:this.attributes.pricelist_id ? this.attributes.pricelist_id : null,
                driver_name: this.getDriver(),
                user_id: this.getUser(),
                table_data: this.getTable(),
                id: this.attributes.id ? this.attributes.id : null,
                split_order: this.attributes.split ? this.attributes.split : null,
                qr_code_id : $("#qr_selection" ).val() ? $("#qr_selection" ).val() : null,
            };
        },
 });

    module.PosWidget.include({
        build_widgets: function(){
            var self = this;
            this._super();
            $( "#order_confirm_button").unbind( "click" );
            $("#order_confirm_button").click(function(e){
                var currentOrder = self.pos.get('selectedOrder');
                if(self.pos.config.is_qr_report){
                    if(! $("#qr_selection" ).val()){
                        alert("Select QR Code !!");
                    }else if(! currentOrder.get_client_name()){
                        alert("Select Partner !!")
                    }else{
                        self.pos.kitchen_receipt = false
                        self.pos.customer_receipt = true
                        if(self.pos.attributes.selectedOrder.attributes.orderLines.models == ''){
                              alert(_t("Can not confirm order which have no order line"))
                        }else{
                            currentOrder.attributes.pricelist_id = parseInt($("#pricelist_selection" ).val())
                            currentOrder.kitchen_receipt = false
                            currentOrder.customer_receipt = true
//                            self.receipt_screen.refresh()
//                            self.pos_widget.screen_selector.set_current_screen('receipt');
                            self.pos_order_dataset.call("create_from_ui", [[currentOrder.exportAsJSON()], false,true]).done(function(order_id){
                                self.pos.attributes.selectedOrder.attributes.id = order_id[0]
                                console.log("self.pos.attributes.selectedOrder.attributes.id",self.pos.attributes.selectedOrder.attributes.id)
                                self.do_action('pos_invoice_report.pos_invoice_anverso_report',{additional_context:{ 
                                    active_ids : [self.pos.attributes.selectedOrder.attributes.id],
                                }});
                            });
                        }
                    }
                }else if(! self.pos.config.is_qr_report){
                	self.pos.kitchen_receipt = false
                    self.pos.customer_receipt = true
                    if(self.pos.attributes.selectedOrder.attributes.orderLines.models == ''){
                          alert(_t("Can not confirm order which have no order line"))
                    }else{
                        currentOrder.attributes.pricelist_id = parseInt($("#pricelist_selection" ).val())
                        currentOrder.kitchen_receipt = false
                        currentOrder.customer_receipt = true
                        self.receipt_screen.refresh()
                        self.pos_widget.screen_selector.set_current_screen('receipt');
                        self.pos_order_dataset.call("create_from_ui", [[currentOrder.exportAsJSON()], false,true]).then(function(order_id){
                            self.pos.attributes.selectedOrder.attributes.id = order_id[0]
                        });
                    }
                }
            })
        },
    });
};


