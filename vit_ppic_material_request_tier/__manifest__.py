# -*- coding: utf-8 -*-
{
    'name': "vit ppic material request tier",

    'summary': """
        Tier validation for material request""",

    'description': """
        Tier validation for material request
    """,

    'author': "My Company",
    'website': "richard.angga51@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tier Validation',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 
        'vit_ppic_material_request',
        'vit_ppic_material_request_inherit', 
        'base_tier_validation',
        'vit_settings_approval',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ppic_material_request.xml',
        'views/data_ppic_material_request_tier.xml',

    ],
    
}
