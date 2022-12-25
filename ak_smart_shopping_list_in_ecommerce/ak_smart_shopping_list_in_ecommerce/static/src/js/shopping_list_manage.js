odoo.define('ak_smart_shopping_list_in_ecommerce.shopping_list_manage', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.websiteSaleShoopingList = publicWidget.Widget.extend({
        selector: '#shipping_list_container',
        events: {
            'click #create_shopping_list': '_onClickCreateShoppingList',
            'click .accordian_cart': '_onClickAddListCart',
            'click .accordian_delete': '_onClickDeleteList',
            'click .add_item_cart': '_onClickAddListLineCart',
            'click .delete_item': '_onClickDeleteListLine',
            'click .js_add_sub_qty': '_onClickQuantity',
        },

        _onClickQuantity: function(ev) {
            var $link = $(ev.currentTarget);
            var $input = $(ev.currentTarget).parent().find('.input_qty');
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
            if (newQty !== previousQty) {
                $input.val(newQty).trigger('change');
            }
            var lineId = $(ev.currentTarget).parents('tr').attr('data-line_id');
            if (lineId) {
                this._rpc({
                    model: 'shopping.list.line',
                    method: 'write',
                    args: [[parseInt(lineId)], {
                       product_qty : parseInt(newQty),
                    }],
                });
            }
        },

        _onClickCreateShoppingList: function(ev) {
            ajax.jsonRpc("/create/shopping/list", 'call', {}).then(function(modal) {
                var $modal = $(modal);
                $modal.modal('show');
            });
        },

        _update_line: async function(ev) {
            var table = $('#shopping_list_table').find('tr');
            for (var i = 0; i < table.length; i++) {
                var line_id = table[i].dataset && table[i].dataset.line_id
                var qty = $(table[i]).find('.input_qty').val();
                await this._rpc({
                    model: 'shopping.list.line',
                    method: 'write',
                    args: [[parseInt(line_id)], {
                       product_qty : parseInt(qty),
                    }],
                });
            };
            return Promise.resolve();
        },

        _onClickAddListCart: function(ev) {
            var defs = [];
            defs.push(this._update_line());
            Promise.all(defs).then(function (e) {
                var list_ids = ev.currentTarget && ev.currentTarget.dataset && ev.currentTarget.dataset.id;
                if (list_ids) {
                    ajax.jsonRpc("/add/cart", 'call', { 'list_ids': parseInt(list_ids) }).then(function(data) {
                        if (!data.cart_quantity) {
                            return window.location = '/shop/cart';
                        };
                    });
                };
            });
        },

        _onClickAddListLineCart: function(ev) {
            var current_ev = ev;
            var self = this;
            var list_line_id = ev.currentTarget && ev.currentTarget.parentNode && ev.currentTarget.parentNode.parentElement && ev.currentTarget.parentNode.parentElement.dataset && ev.currentTarget.parentNode.parentElement.dataset.line_id;
            var qty = $(ev.currentTarget).parents('#line_id').find('.input_qty').val();
            
            if (list_line_id) {
                ajax.jsonRpc("/add/cart", 'call', { 'list_line_id': parseInt(list_line_id), 'qty': parseInt(qty) }).then(function(data) {
                    var list_line_id = current_ev.currentTarget && current_ev.currentTarget.parentNode && current_ev.currentTarget.parentNode.parentElement && current_ev.currentTarget.parentNode.parentElement.dataset && current_ev.currentTarget.parentNode.parentElement.dataset.line_id;
                    var qty = $(current_ev.currentTarget).parents('#line_id').find('.input_qty').val();
                    if (!data.cart_quantity) {
                        self._rpc({
                            model: 'shopping.list.line',
                            method: 'write',
                            args: [[parseInt(list_line_id)], {
                               product_qty : parseInt(qty),
                            }],
                        });
                        return window.location = '/my/shopping/list';
                    };
                });
            };
        },

        _onClickDeleteList: function(ev) {
            var delete_list_id = ev.currentTarget && ev.currentTarget.dataset && ev.currentTarget.dataset.id;
            if (delete_list_id) {
                ajax.jsonRpc("/remove/list/dialog", 'call', { 'list_id': parseInt(delete_list_id) }).then(function(modal) {
                    var $modal = $(modal);
                    $modal.modal('show');
                });
            };
        },

        _onClickDeleteListLine: function(ev) {

            var current_ev = ev;
            var remove_line_id = ev.currentTarget && ev.currentTarget.parentNode && ev.currentTarget.parentNode.parentElement && ev.currentTarget.parentNode.parentElement.dataset && ev.currentTarget.parentNode.parentElement.dataset.line_id;
            if (remove_line_id) {
                ajax.jsonRpc("/remove/list/line", 'call', { 'list_line_id': parseInt(remove_line_id) }).then(function(data) {
                    var $item = data.shopping_list_item_count;
                    var $target_card = $(current_ev.currentTarget).parents('.shopping_list_card');
                    var $target_tr = $(current_ev.currentTarget).parents('tr');
                    var $target_card_body = $(current_ev.currentTarget).parents('.shopping_list_card_body');
                    
                    if ($item == 0) {
                        $target_card.find('.product_item span').text($item);
                        $target_card.find('.mobile_product_item span').text($item);
                        $target_card_body.hide('slow', function(){ $target_card_body.remove(); });
                        $target_card.find('.accordion_button').attr('disabled', 'disabled');
                        $target_card.find('.accordian_cart').attr('disabled', 'disabled');
                    } else {
                        $target_card.find('.product_item span').text($item);
                        $target_card.find('.mobile_product_item span').text($item);
                        $target_tr.hide('slow', function(){ $target_tr.remove(); });
                    }
                });
            }
        },

    });
});
