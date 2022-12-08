# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Odoo Website Show Packaging Options",
  "summary"              :  """Odoo Website Show Packaging Options in Odoo facilitates the creation of Packaging-based products in the Odoo.""",
  "category"             :  "Sales",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Odoo-Website-Show-Packaging-Options.html",
  "description"          :  """Odoo Website Show Packaging Options""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=Odoo_Website_Show_Packaging_Options&version=13.0&custom_url=/shop/",
  "depends"              :  [
                             'website_sale',
                             'Odoo_Merge_Similar_packaging_orders',
                            ],
  "data"                 :  ['views/website_template_inherit.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  10,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}