# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software.
# mail:   odoo@aktivsoftware.com
# Copyright (C) 2021-Present Aktiv Software.
# Contributions:
#           Aktiv Software:
#              - Burhan Vakharia
#              - Helly Kapatel, Aarti Sathvara
#              - Tanvi Gajera

{
    "name": "Smart Shopping List In Ecommerce",
    "author": "Aktiv Software",
    "website": "http://www.aktivsoftware.com",
    "summary": """
        smart list,
        shopping list,
        quick shopping list,
        smart shopping list,
        add product in list,
        add product in shopping list,
        wish list,
        want list,
        basket list,
        hit-list,
        favourites list,
        wanted list,
        wish shopping list,
        want shopping list,
        basket shopping list,
        hit-list shopping,
        favourites shopping list,
        wanted shopping list,
        laundry list,
        order of the day list,
        order of the month list,
        laundry shopping list,
        bucket shopping list,
        bucket list,
        catalog list,
        virtual shopping list,
        daily need list,
        daily list,
    """,
    "description": """
        Title: Users can create a shopping list of their own choice from
        website portal itself.
        Author: Aktiv Software
        mail: odoo@aktivsoftware.com
        Copyright (C) 2021-Present Aktiv Software PVT. LTD.
        Contributions: Aktiv Software
    """,
    "license": "OPL-1",
    "category": "Website Sale",
    "version": "15.0.1.0.0",
    "price": "10.00",
    "currency": "EUR",
    "depends": ["website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/shopping_list_view.xml",
    ],
    "images": ["static/description/banner.jpeg"],
    "installable": True,
    "auto_install": False,
    'assets': {
        'web.assets_frontend': [
            'ak_smart_shopping_list_in_ecommerce/static/src/js/**/*',
        ],

    },
}
