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
                raw_data += "<tr><td>"+line.product_id.name+"</td><td>"+line.name+"</td><td>"+str(line.product_uom_qty)+"</td><td>"+str(line.product_packaging.name)+"</td><td>"+str(int((line.product_uom_qty)/(line.product_packaging.qty)))+" Packages</td><td>"+str(line.price_subtotal)+"</td></tr>"

        self.description=html_data+raw_data+"</tbody></table>"



    def _get_move_ids_without_package(self):
        self.ensure_one()

        move_ids_without_package = self.env['stock.move']
        if not self.picking_type_entire_packs:
            move_ids_without_package = self.move_lines
        else:
            for move in self.move_lines:
                if not move.package_level_id:
                    if move.state in ('assigned', 'done'):
                        if any(not ml.package_level_id for ml in move.move_line_ids):
                            move_ids_without_package |= move
                    else:
                        move_ids_without_package |= move
        
        automatic_merger = self.env['res.config.settings'].sudo().get_values()['automatic_merge']
        if automatic_merger:
            product_ids= [move.product_id.id for move in self.move_lines]
            
            move_ids_without_package = move_ids_without_package.filtered(lambda move: True if not move.product_id.packaging_ids else False)
            self.move_lines = self.move_lines.filtered(lambda move: True if move.product_id.id in product_ids and  move.product_id.packaging_ids else False)
            flag = {i.product_id.name:[product_ids.count(i.product_id.id),0,0,0] for i in self.move_lines}
            obj=None
            newely_created = set()
            for move in  self.move_lines:
                product_obj =move.product_id
                if product_ids.count(move.product_id.id)>=2 or move.product_id.packaging_ids:
                    flag[move.product_id.name][0] = flag[move.product_id.name][0]-1
                    flag[move.product_id.name][1] = flag[move.product_id.name][1] + move.product_uom_qty
                    flag[move.product_id.name][2] = flag[move.product_id.name][2]+ move.reserved_availability
                    flag[move.product_id.name][3] = flag[move.product_id.name][3] +move.quantity_done
                    move.state='draft'
                    move.unlink()
                else:
                    flag[move.product_id.name][1] = move.product_uom_qty
                    flag[move.product_id.name][2] = move.reserved_availability
                    flag[move.product_id.name][3] = move.quantity_done
                if flag[product_obj.name][0] == 0 :
                    obj=self.env['stock.move'].sudo().create({
                    'name': product_obj.name,
                    'location_id': self.location_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'product_id': product_obj.id,
                    'product_uom_qty': flag[product_obj.name][1],
                    'product_uom': product_obj.uom_id.id,
                    'reserved_availability':  flag[product_obj.name][2],
                    'quantity_done': flag[product_obj.name][3],
                    'origin':self.origin,
                    })
                    
                if obj:
                    newely_created = newely_created.union(obj)
            if newely_created:
                for i in newely_created:
                    move_ids_without_package += i
                self.move_lines = move_ids_without_package
            else:
                self.move_lines = move_ids_without_package.union(self.move_lines)
                move_ids_without_package = self.move_lines
        self.state = 'waiting'

        return move_ids_without_package.filtered(lambda move: not move.scrap_ids) 
