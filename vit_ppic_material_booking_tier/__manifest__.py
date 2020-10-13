# -*- coding: utf-8 -*-
{
    'name': "vit_ppic_material_booking_tier",

    'summary': """
        Tier validation for ppic material_booking""",

    'description': """
        Tier validation for ppic material_booking
    """,

    'author': "My Company",
    'website': "richard.angga51@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 
        'vit_ppic_material_booking',
        'vit_ppic_material_booking_inherit', 
        'base_tier_validation'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/material_booking.xml',
        'views/data_tier.xml',

    ],
    
}
