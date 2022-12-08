# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "Website Product Dimensions(Height/Width)",
    'version': "16.0.0.0",
    'category': "Website",
    'license': 'OPL-1',
    'summary': "Sale product Dimension purchase product Dimension product height and width product width on product height attribute product Width attribute website products dimension on website dimension webshop product dimension ecommerce product dimension on sales",
    'description': """With this application, you can set the variable Height & Width from the website sales order and get the net price based on dimension.""",
    'author': "BrowseInfo",
    "website": "https://www.browseinfo.in",
    "price": 70,
    'currency': "EUR",
    'depends': ['website_sale', 'bi_product_dimension'],
    'data': ['views/templates.xml',
             'views/res_config_settings_views.xml'],
    'assets': {
        'web.assets_frontend': [
            "/bi_website_dimension/static/src/js/web_product_dimension.js"
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    "live_test_url": 'https://youtu.be/_o5XE4Fz8Gg',
    "images": ["static/description/Banner.png"],
}
