# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_website_dimension = fields.Boolean(string='Product Dimension on Website',
                                               config_parameter='bi_website_dimension.enable_website_product_dimension')

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('bi_website_dimension.enable_website_product_dimension',
                                                         False)
        super(ResConfigSettings, self).set_values()
