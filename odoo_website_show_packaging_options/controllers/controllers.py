# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from datetime import datetime, timedelta
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website
from odoo import http
from odoo.http import request
import logging
import json
_logger = logging.getLogger(__name__)


class Website(WebsiteSale):

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(
                kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(
                kw.get('no_variant_attribute_values'))
        
        if request.env['product.product'].sudo().browse([int(product_id)]).packaging_ids:
            sale_order._cart_update(
                product_id=int(product_id),
                add_qty=add_qty,
                set_qty= int(request.env['product.packaging'].sudo().browse(int(kw.get('attrib'))).qty)*int(add_qty) if kw.get('attrib') else set_qty ,
                product_custom_attribute_values=product_custom_attribute_values,
                no_variant_attribute_values=no_variant_attribute_values,
                line_id=False,
                kwargs=kw
            )
        else:
            sale_order._cart_update(
                product_id=int(product_id),
                add_qty=add_qty,
                set_qty=set_qty,
                product_custom_attribute_values=product_custom_attribute_values,
                no_variant_attribute_values=no_variant_attribute_values,
            )

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")
        
