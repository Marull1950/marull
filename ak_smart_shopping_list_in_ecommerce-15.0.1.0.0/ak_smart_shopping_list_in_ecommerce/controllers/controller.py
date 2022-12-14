# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import http, fields
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @http.route(["/my/shopping/list"], type="http", auth="user", website=True)
    def my_shopping_list(self, **kw):
        shopping_lists = (
            request.env["shopping.list"]
            .sudo()
            .search([("user_id", "=", request.env.user.id)])
        )
        values = {"shopping_lists": shopping_lists}
        return request.render(
            "ak_smart_shopping_list_in_ecommerce.my_shopping_list_template", values
        )

    @http.route(
        ["/create/shopping/list"],
        type="json",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def create_shopping_list(self, **kw):
        return request.env["ir.ui.view"]._render_template(
            "ak_smart_shopping_list_in_ecommerce.create_shopping_list_dialog"
        )

    @http.route(["/shopping/list/submit"], type="http", auth="user", website=True)
    def shopping_list_submit(self, **kw):
        vals = {"name": kw.get("list_name"), "user_id": request.env.user.id}
        request.env["shopping.list"].sudo().create(vals)
        return request.redirect("/my/shopping/list")

    @http.route(
        ["/add/shopping/list"], type="json", auth="user", methods=["POST"], website=True
    )
    def add_shooping_list(self, **kw):
        vals = {}
        product_id = False
        if kw.get("product_id"):
            product_id = int(kw.get("product_id"))

        shopping_list_ids = (
            request.env["shopping.list"]
            .sudo()
            .search([("user_id", "=", request.env.user.id)])
        )
        if not shopping_list_ids:
            vals = {"name": "My Shopping List", "user_id": request.env.user.id}
            shopping_list_ids = request.env["shopping.list"].sudo().create(vals)

        vals = {
            "shopping_list_ids": shopping_list_ids,
            "product_id": product_id,
            "current_url": kw.get("current_url"),
        }
        return request.env["ir.ui.view"]._render_template(
            "ak_smart_shopping_list_in_ecommerce.add_product_shopping_list", vals
        )

    @http.route(["/add/shopping/list/submit"], type="http", auth="user", website=True)
    def add_shopping_list_submit(self, **kw):
        vals = {}
        current_url = ""
        if kw.get("current_url"):
            current_url = kw.get("current_url")

        if kw.get("list_id"):
            if kw.get("list_record"):
                shopping_list_line_obj = (
                    request.env["shopping.list.line"]
                    .sudo()
                    .browse(int(kw.get("list_record")))
                )
                shopping_list_line_obj.sudo().update(
                    {
                        "product_qty": shopping_list_line_obj.product_qty
                        + int(kw.get("input_qty")),
                    }
                )
            else:
                vals.update(
                    {
                        "product_id": int(kw.get("product_id")),
                        "shopping_list_id": int(kw.get("list_id")),
                        "product_qty": int(kw.get("input_qty")),
                    }
                )
                request.env["shopping.list.line"].sudo().create(vals)
        return request.redirect(current_url)

    @http.route(["/select_shopping_list"], type="json", auth="user", website=True)
    def select_shopping_list(self, **kw):

        if kw.get("product_id") and kw.get("select_line_id"):
            product_id = int(kw.get("product_id"))
            select_line_id = int(kw.get("select_line_id"))

        list_record = (
            request.env["shopping.list.line"]
            .sudo()
            .search(
                [
                    "&",
                    ("shopping_list_id", "=", select_line_id),
                    ("product_id", "=", product_id),
                ],
                order="id desc",
                limit=1,
            )
        )
        vals = {}
        if list_record:
            vals.update({"list_record": list_record.id})
            return vals
        return False

    @http.route(["/add/cart"], type="json", auth="user", website=True)
    def add_cart(self, display=True, **kw):
        list_ids = False

        if kw.get("list_ids"):
            list_ids = request.env["shopping.list.line"].search(
                [("shopping_list_id", "=", int(kw.get("list_ids")))]
            )
        elif kw.get("list_line_id"):
            list_id = request.env["shopping.list.line"].search(
                [("id", "=", int(kw.get("list_line_id")))]
            )

        value = {}
        order = request.website.sale_get_order(force_create=1)

        if order.state != "draft":
            request.website.sale_reset()
            return {}
        if list_ids and len(list_ids) >= 1:
            for l in list_ids:
                value = order._cart_update(
                    product_id=l.product_id.id, add_qty=l.product_qty
                )
        else:
            if kw.get("qty"):
                value = order._cart_update(
                    product_id=list_id.product_id.id, add_qty=kw.get("qty")
                )

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value["cart_quantity"] = order.cart_quantity

        if not display:
            return value

        value["website_sale.cart_lines"] = request.env["ir.ui.view"]._render_template(
            "website_sale.cart_lines",
            {
                "website_sale_order": order,
                "date": fields.Date.today(),
                "suggested_products": order._cart_accessories(),
            },
        )
        value["website_sale.short_cart_summary"] = request.env[
            "ir.ui.view"
        ]._render_template(
            "website_sale.short_cart_summary",
            {
                "website_sale_order": order,
            },
        )

        return request.env["ir.ui.view"]._render_template("website_sale.cart", value)

    @http.route(["/remove/list/line/"], type="json", auth="user", website=True)
    def remove_list_line(self, **kw):
        if kw.get("list_line_id"):
            line_rec = (
                request.env["shopping.list.line"]
                .sudo()
                .browse(int(kw.get("list_line_id")))
            )
            shopping_list_rec = line_rec.shopping_list_id
            line_rec.unlink()

        return {"shopping_list_item_count": len(shopping_list_rec.line_ids)}

    @http.route(["/remove/list/dialog"], type="json", auth="user", website=True)
    def remove_list_dialog(self, **kw):
        vals = {}
        if kw.get("list_id"):
            vals = {"list_id": int(kw.get("list_id"))}
        return request.env["ir.ui.view"]._render_template(
            "ak_smart_shopping_list_in_ecommerce.remove_shopping_list", vals
        )

    @http.route(["/remove/list"], type="http", auth="user", website=True)
    def remove_list(self, **kw):
        if kw.get("list_id"):
            list_rec = (
                request.env["shopping.list"].sudo().browse(int(kw.get("list_id")))
            )
            list_rec.unlink()
        return request.redirect("/my/shopping/list")
