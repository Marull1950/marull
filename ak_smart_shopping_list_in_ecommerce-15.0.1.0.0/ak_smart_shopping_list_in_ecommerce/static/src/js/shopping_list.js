odoo.define('ak_smart_shopping_list_in_ecommerce.shopping_list', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.websiteCreateShoppingList = publicWidget.Widget.extend({
        selector: '#wishlist_btn',
        events: {
            'click': '_onClick',
        },

        _onClick: function(ev) {
            var product_id = $('.js_product').find('.product_id').val();
            var current_url = new URL(window.location.href).pathname;
            ajax.jsonRpc("/add/shopping/list", 'call', { 'product_id': parseInt(product_id), 'current_url': current_url }).then(function(modal) {
                var $modal = $(modal);
                $modal.modal('show');

                var selected_line_id = $("#list_id").children(":selected").val();
                if (selected_line_id) {
                    ajax.jsonRpc("/select_shopping_list", 'call', { 'product_id': parseInt(product_id), 'select_line_id': selected_line_id }).then(function(data) {
                        $modal.find('#list_record').val(data.list_record);
                        if (data) {
                            $('#msg').text("This product has been already added to the selected shopping list.");
                        } else {
                            $('#msg').text('');
                        };
                    });
                };

                $("#list_id").on('change', function(event) {
                    var select_line_id = $(this).children(":selected").val();
                    if (select_line_id) {
                        ajax.jsonRpc("/select_shopping_list", 'call', { 'product_id': parseInt(product_id), 'select_line_id': parseInt(select_line_id), }).then(function(data) {
                            $modal.find('#list_record').val(data.list_record);
                            if (data) {
                                $('#msg').text("This product has been already added to the selected shopping list.");
                            } else {
                                $('#msg').text('');
                            };
                        });
                    };
                });

                $(".sub_qty_shoppinglist").on('click', function(event) {
                    var $link = $('.sub_qty_shoppinglist');
                    var $input = $('.input_qty');
                    var min = parseFloat($input.data("min") || 0);
                    var max = parseFloat($input.data("max") || Infinity);
                    var previousQty = parseFloat($input.val() || 0, 10);
                    var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
                    var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
                    if (newQty !== previousQty) {
                        $input.val(newQty).trigger('change');
                    }
                    return false;
                });

                $(".add_qty_shoppinglist").on('click', function(event) {
                    var $link = $('.add_qty_shoppinglist');
                    var $input = $('.input_qty');
                    var min = parseFloat($input.data("min") || 0);
                    var max = parseFloat($input.data("max") || Infinity);
                    var previousQty = parseFloat($input.val() || 0, 10);
                    var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
                    var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
                    if (newQty !== previousQty) {
                        $input.val(newQty).trigger('change');
                    }
                    return false;
                });

                $modal.on('click', '.modal_close', function(e) {
                    location.reload();
                });
            });
        },
    });
});
