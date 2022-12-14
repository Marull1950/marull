# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import models, fields


class ShoppingList(models.Model):
    _name = "shopping.list"
    _description = "Shopping List"

    name = fields.Char(string="Name")
    user_id = fields.Many2one("res.users", string="User")
    line_ids = fields.One2many(
        "shopping.list.line", "shopping_list_id", string="Lsit Line"
    )
    total_items = fields.Integer(string="Total Items", compute="_compute_total_product")

    def _compute_total_product(self):
        for rec in self:
            rec.total_items = False
            if rec.line_ids:
                rec.total_items = len(rec.line_ids)


class ShoppingListline(models.Model):
    _name = "shopping.list.line"
    _description = "Shopping List Line"

    product_id = fields.Many2one("product.product", string="Product")
    product_qty = fields.Integer(string="Quantity")
    shopping_list_id = fields.Many2one("shopping.list", string="Shopping List")
