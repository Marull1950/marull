# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today  Technaureus Info Solutions(<http://technaureus.com/>).
from odoo import models,fields


class Website(models.Model):
    _inherit = 'website'

    # hide_price = fields.Boolean("Hide Price", default=True)
    cart_hide_price = fields.Boolean("Hide Price", default=True)
    optional_product_hide = fields.Boolean("Hide Optional Product Price", default=True)


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    # hide_price = fields.Boolean("Hide Price", default=True)
    cart_hide_price = fields.Boolean(related='website_id.cart_hide_price', readonly=False)
    optional_product_hide = fields.Boolean(related='website_id.optional_product_hide', readonly=False)
