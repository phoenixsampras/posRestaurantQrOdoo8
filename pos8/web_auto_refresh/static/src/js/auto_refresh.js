openerp.web_auto_refresh = function(instance) {

    instance.web.ViewManager.include({
        switch_mode: function(view_type, no_store, view_options) {
            var self = this;
            var view = this.views[view_type];
            var view_promise;
            var form = this.views['form'];
            if (!view || (form && form.controller && !form.controller.can_be_discarded())) {
                return $.Deferred().reject();
            }
            if (!no_store) {
                this.views_history.push(view_type);
            }
            this.active_view = view_type;

            if (!view.controller) {
                view_promise = this.do_create_view(view_type);
            } else if (this.searchview
                    && self.flags.auto_search
                    && view.controller.searchable !== false) {
                this.searchview.ready.done(this.searchview.do_search);
            }

            if (this.searchview) {
                this.searchview[(view.controller.searchable === false || this.searchview.options.hidden) ? 'hide' : 'show']();
            }

            console.log("FFFFFFFFFFFFFFFFFFFFFFFFF")
            self.set_auto_refresh();
            this.$el.find('.oe_view_manager_switch a').parent().removeClass('active');
            this.$el
                .find('.oe_view_manager_switch a').filter('[data-view-type="' + view_type + '"]')
                .parent().addClass('active');
            this.$el.attr("data-view-type", view_type);
            return $.when(view_promise).done(function () {
                _.each(_.keys(self.views), function(view_name) {
                    var controller = self.views[view_name].controller;
                    if (controller) {
                        var container = self.$el.find("> div > div > .oe_view_manager_body > .oe_view_manager_view_" + view_name);
                        if (view_name === view_type) {
                            container.show();
                            controller.do_show(view_options || {});
                        } else {
                            container.hide();
                            controller.do_hide();
                        }
                    }
                });
                self.trigger('switch_mode', view_type, no_store, view_options);
            });
        },
        set_auto_refresh: function(){
            var self = this
            console.log("refreshhhhhhhhhhhhhhhhhh",self.action)
            if(self.action && self.action.auto_refresh){
            	console.log("")
                setTimeout(function(){
                    self.searchview.ready.done(self.searchview.do_search);
                    self.set_auto_refresh()
                }, self.action.auto_refresh);
            }
        },
    });
}
