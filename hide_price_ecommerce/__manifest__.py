# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today  Technaureus Info Solutions(<http://technaureus.com/>).
{
    'name': 'Hide Price Ecommerce(Internal Product Requisition)',
    'version': '16.0.0.0',
    'sequence': 1,
    'category': 'Website',
    'summary': 'Hide Price in Ecommerce- Internal Product Requisition',
    'description': """
    This module helps to hide the price in ecommerce and with this 
    we can utilize for internal product requisition.
    """,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'depends': ['website', 'website_sale'],
    'price': 25,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'views/templates.xml',
        'views/res_config_settings.xml',
    ],
    'images': ['images/main_screenshot.png'],
    "installable": True,
    'application': True,
    'auto_install': False,
    # 'live_test_url': 'https://www.youtube.com/watch?v=m4eKieNvruk&t=6s'
}
