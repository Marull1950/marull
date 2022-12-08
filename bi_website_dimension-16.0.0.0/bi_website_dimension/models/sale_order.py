# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """
        @desc: To update the product dimension based on user inserts values on textbox.
        @args: product_id - int: current product id.
               line_id - int: current order line id.
               add_qty - float: user inserts quantity of related product.
               set_qty - float: exact quantity for current product.
               kwargs - dict: for existing inputs which are given by users.
        @return: super base method with updated product dimensions.
        """
        res = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        quantity = res.get('quantity', 0)
        order_line = res.get('line_id', None) and self.env['sale.order.line'].sudo().browse(int(res.get('line_id'))) or None
        if order_line and quantity > 0:
            order_line.sudo().write({'height': kwargs.get('height', 0.00) or order_line.height,
                                     'width': kwargs.get('width', 0.00) or order_line.width})
        return res
