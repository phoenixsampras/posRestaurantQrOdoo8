(function($) {
$.widget("ui.combobox", {
    options: {
        target: '',
        allowUserValues: true,
    },
    _create: function() {
        var self = this,
            options = this.options,
            select = this.element.hide(),
            selected = select.children(":selected"),
            input = $(options.target), // your input box
            value = selected.val() ? selected.text() : input.val();
        input
            .insertAfter(select)
            .val(value)
            .autocomplete({
                delay: 0,
                minLength: 0,
                source: function(request, response) {
                    var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
                    response(select.children("option").map(function() {
                        var text = $(this).val();
                        if (this.value && (!request.term || matcher.test(text)))
                            return {
                                label: $(this).text().replace(
                                    new RegExp(
                                        "(?![^&;]+;)(?!<[^<>]*)(" +
                                            $.ui.autocomplete.escapeRegex(request.term) +
                                                ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                    ), "<strong>$1</strong>"),
                                value: $(this).text(),
                                option: this
                            };
                    }));
                },
                select: function(event, ui) {
                    ui.item.option.selected = true;
                    self._trigger("selected", event, {
                        item: ui.item.option
                    });
                },
                change: function(event, ui) {

                    if (!ui.item) {
                        var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i"),
                            valid = false;
                        select.children("option").each(function() {
                            if ($(this).text().match(matcher)) {
                                this.selected = valid = true;
                                return false;
                            }
                        });
                        // if allowUserValues, then ignores if user entered value exists in select list and just allow the user entered value
                        if (!options.allowUserValues) {
                            if (!valid) {
                                // remove invalid value, as it didn't match anything
                                $(this).val("");
                                select.val("");
                                input.data("autocomplete").term = "";
                                return false;
                            }
                        }
                    }
                }
            })
            .addClass("ui-widget ui-widget-content ui-corner-left");
        input.data("autocomplete")._renderItem = function(ul, item) {
        	ul.css('height','150px')
        	ul.css('overflow','auto')
            return $("<li'></li>")
                .data("item.autocomplete", item)
                .append("<a>" + item.label + "</a>")
                .appendTo(ul);
        };

        this.button = $("<button type='button'>&nbsp;</button>")
            .attr("tabIndex", -1)
            .attr("title", "Show All Items")
            .insertAfter(input)
            .button({
                icons: {
                primary: "ui-icon-triangle-1-s"
            },
            text: false
            })
            .addClass("")
            .click(function() {
                // close if already visible
                if (input.autocomplete("widget").is(":visible")) {
                    input.autocomplete("close");
                    return;
                }

                // work around a bug (likely same cause as #5265)
                $(this).blur();

                // pass empty string as value to search for, displaying all results
                input.autocomplete("search", "");
                input.focus();
            });
    },

    destroy: function() {
        this.input.remove();
        this.button.remove();
        this.element.show();
        $.Widget.prototype.destroy.call(this);
    }
});
})(jQuery);

