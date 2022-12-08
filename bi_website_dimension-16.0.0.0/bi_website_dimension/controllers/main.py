# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import json

from odoo import http, fields
from odoo.http import request
from odoo.tools.json import scriptsafe as json_scriptsafe
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteProductDimension(WebsiteSale):

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        """
        @desc: When adding a product to cart, update the product dimensions based on user inputs.
        @args: product_id - int: current product id.
               line_id - int: current order line id.
               add_qty - float: user inserts quantity of related product.
               set_qty - float: exact quantity for current product.
               kw - dict: for existing inputs which are given by users.
        @return: redirect to shopping cart page.
        """
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=1)
            else:
                return {}

        is_param = request.env['ir.config_parameter'].sudo().get_param(
            'bi_website_dimension.enable_website_product_dimension', False)
        height = 0.00
        width = 0.00
        if is_param:
            if kw.get('height', False):
                height = json.loads(kw.get('height'))

            if kw.get('width', False):
                width = json.loads(kw.get('width'))

        pcav = kw.get('product_custom_attribute_values')
        nvav = kw.get('no_variant_attribute_values')
        value = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
            no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None,
            height=height,
            width=width
        )

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template("website_sale.short_cart_summary", {
            'website_sale_order': order,
        })
        return value
