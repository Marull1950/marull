#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res =  super(SaleOrder,self)._cart_update(product_id=product_id, line_id=line_id,add_qty=add_qty, set_qty=set_qty,**kwargs)
        if self.env['sale.order.line'].sudo().browse([int(res.get('line_id'))]).exists():
            lines = self.env['sale.order.line'].sudo().browse([int(res.get('line_id'))])
            if kwargs.get('kwargs'):
                if lines.product_id.packaging_ids and kwargs.get('kwargs').get('attrib'):
                    lines.write({'product_packaging':int(kwargs.get('kwargs').get('attrib'))})
        
        return res




