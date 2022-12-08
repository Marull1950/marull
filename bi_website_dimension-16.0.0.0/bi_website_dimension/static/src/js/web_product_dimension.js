odoo.define('bi_website_dimension.calculate_product_price', function (require) {
'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var utils = require('web.utils');
    var publicWidget = require('web.public.widget');
	var WebsiteSale = require('website_sale.website_sale');
    var _t = core._t;

    // Calculate the m2 price based on user insert Height & Width
    $("#calculate_price").click(function(){

        var height = $("input[name=height]").val()
        var width = $("input[name=width]").val()
        var $price = $(".oe_price:first .oe_currency_value");
        var $total_price = parseFloat(height) * parseFloat(width) * parseFloat($price.text().replace(",",""))

        if ($total_price){
            $("input[name=height], input[name=width]").css('border', "");
            $('.price_label').html('Dimension(m2) Price')
            $('.oe_dimension_price').html(_priceToStr($total_price));
        }
        else{
           $("input[name=height], input[name=width]").css('border', "2px solid red");
           $('.price_label, .oe_dimension_price').html('')
        }

    })

    // Allow only numbers for both input boxes
    $("input[name=height], input[name=width]").keydown(function (event) {
        if (event.shiftKey == true) {
            event.preventDefault();
        }
        if ((event.keyCode >= 48 && event.keyCode <= 57) ||
            (event.keyCode >= 96 && event.keyCode <= 105) ||
            event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 37 ||
            event.keyCode == 39 || event.keyCode == 46 || event.keyCode == 190) {

        } else {
            event.preventDefault();
        }
        if($(this).val().indexOf('.') !== -1 && event.keyCode == 190)
            event.preventDefault();
    });

    // Convert price to str to maintain odoo standard price
    function _priceToStr(price){
        var l10n = _t.database.parameters;
        var precision = 2;

        if ($('.decimal_precision').length) {
            precision = parseInt($('.decimal_precision').last().data('precision'));
        }
        var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
        formatted[0] = utils.insert_thousand_seps(formatted[0]);
        return formatted.join(l10n.decimal_point);
    }

    publicWidget.registry.WebsiteSale.include({
        _handleAdd: function ($form) {
        var self = this;
        this.$form = $form;

        var productSelector = [
            'input[type="hidden"][name="product_id"]',
            'input[type="radio"][name="product_id"]:checked'
        ];
        var height = $form.find('input[name="height"]').val();
        var width = $form.find('input[name="width"]').val();

        var productReady = this.selectOrCreateProduct(
            $form,
            parseInt($form.find(productSelector.join(', ')).first().val(), 10),
            $form.find('.product_template_id').val(),
            false
        );

        return productReady.then(function (productId) {
            $form.find(productSelector.join(', ')).val(productId);

            self.rootProduct = {
                product_id: productId,
                quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
                product_custom_attribute_values: self.getCustomVariantValues($form.find('.js_product')),
                variant_values: self.getSelectedVariantValues($form.find('.js_product')),
                no_variant_attribute_values: self.getNoVariantAttributeValues($form.find('.js_product')),
                height:height,
                width:width
            };

            return self._onProductReady();
        });}
    });
});
