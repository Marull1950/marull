# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from functools import reduce


import logging

_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_manufacture(self, procurements):
        automatic_merger = self.env['res.config.settings'].sudo().get_values()['automatic_merge']
        if automatic_merger:
            flag = {procurement.product_id.id: []
                    for procurement, rule in procurements}
            for procurement, rule in procurements:
                if len(flag[procurement.product_id.id]) == 0:
                    flag[procurement.product_id.id] = (procurement, rule)
        
                else:
                    test = flag[procurement.product_id.id][0]
                    flag[procurement.product_id.id] = (test._replace(
                        product_qty=flag[procurement.product_id.id][0].product_qty + procurement.product_qty), rule)
        
            procurements = [(value[0], value[1]) for key, value in flag.items()]
        return super(StockRule,self)._run_manufacture(procurements)



class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'


    description_mrp =fields.Html(string='Description',compute="_compute_description_mrp")


    def _compute_description_mrp(self):
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
        for line in self.env['sale.order'].sudo().search([('name','=',self.origin)]).order_line.filtered(lambda line: True if line.product_id.id ==self.product_id.id else False):
            raw_data += "<tr><td>"+line.product_id.name+"</td><td>"+line.name+"</td><td>"+str(line.product_uom_qty)+"</td><td>"+str(line.product_packaging.name)+"</td><td>"+str(int((line.product_uom_qty)/(line.product_packaging.qty)))+" Packages</td><td>"+str(line.price_subtotal)+"</td></tr>"

        self.description_mrp=html_data+raw_data+"</tbody></table>"



    def action_merge_mo(self):

        filtered_record = {rec.product_id.name+' '+rec.origin:[self.search([('product_id','=',rec.product_id.id),('origin','=',rec.origin),('state','=','confirmed')])] for rec in self}
        temp=dict()
        for key,value in filtered_record.items():  
            if len(value[0])>1:
                temp[key]=value
        for key,value in temp.items():
            product_qty=0
            for val in value[0]:
                val_create={
                        'origin': val.origin,
                        'product_id': val.product_id.id,
                        'product_uom_id': val.product_uom_id.id,
                        'location_src_id': val.location_src_id.id or val.picking_type_id.default_location_src_id.id,
                        'location_dest_id': val.location_dest_id.id,
                        'bom_id': val.bom_id.id,
                        'date_deadline': val.date_deadline,
                        'date_planned_finished': val.date_planned_finished,
                        'date_planned_start': val.date_planned_start,
                        'procurement_group_id': val.procurement_group_id.id,
                        'propagate_cancel': val.propagate_cancel,
                        'propagate_date': val.propagate_date,
                        'propagate_date_minimum_delta': val.propagate_date_minimum_delta,
                        'orderpoint_id': val.orderpoint_id.id,
                        'picking_type_id': val.picking_type_id.id,
                        'company_id': val.company_id.id,
                        'move_dest_ids': val.move_dest_ids,
                        'user_id': False,
                        'state':val.state,
                        'reservation_state':val.reservation_state,
                }
                product_qty+=val.product_qty
                val.action_cancel()
            val_create.update({'product_qty': product_qty})
            production=val.env['mrp.production'].sudo().create(val_create)
            self.env['stock.move'].sudo().create(production._get_moves_raw_values())
            production.action_confirm()

    
