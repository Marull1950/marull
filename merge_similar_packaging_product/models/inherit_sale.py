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
    _inherit = 'sale.order'

    def action_confirm(self):
        automatic_merger = self.env['res.config.settings'].sudo().get_values()['automatic_merge']
        if automatic_merger:
            pack_products_line = self.order_line.filtered(lambda line: True if line.product_packaging.id in line.product_id.packaging_ids.ids else False)
            diff_line = self.order_line - pack_products_line
            products = pack_products_line.mapped('product_id')

            filter_sol = {product.id:[self.order_line.filtered(lambda line: True if line.product_id.id == product.id else False)] for product in products }

            for key,value in filter_sol.items():
                qty=sum(value[0].mapped('product_uom_qty'))
                value[0][0].write({'product_uom_qty': qty})
                filter_sol[key] = value[0][0]
            for k,v in filter_sol.items():
                diff_line=diff_line.union(filter_sol[k][0])
            self.order_line = diff_line

        return super(SaleOrder,self).action_confirm()



class Picking(models.Model):
    _inherit = 'stock.picking'


    description =fields.Html(string='Description',compute="_compute_description")


    def _compute_description(self):
        html_data = '''<table class="table">
                        <thead>
                                <tr>
                                    <th>Product Name</th>
                                    <th>Product Description</th>
                                    <th>Quantity</th>
                                    <th>Unit pack</th>
                                    <th>Package to be delivered</th>
                                    <th>Subtotal</th>
                                </tr>
                        </thead>
                        <tbody>
                                            
                                            '''
        raw_data=""
        for line in self.env['sale.order'].sudo().search([('name','=',self.origin)]).order_line: 
            if line.product_id.packaging_ids:
                if line.product_packaging.qty!=0:
                    raw_data += "<tr><td>"+line.product_id.name+"</td><td>"+line.name+"</td><td>"+str(line.product_uom_qty)+"</td><td>"+str(line.product_packaging.name)+"</td><td>"+str(int((line.product_uom_qty)/(line.product_packaging.qty)))+" Packages</td><td>"+str(line.price_subtotal)+"</td></tr>"
                else:
                    raw_data += "<tr><td>"+line.product_id.name+"</td><td>"+line.name+"</td><td>"+str(line.product_uom_qty)+"</td><td>"+str(line.product_packaging.name)+"</td><td>"+str(line.product_uom_qty)+" Packages</td><td>"+str(line.price_subtotal)+"</td></tr>"


        self.description=html_data+raw_data+"</tbody></table>"



