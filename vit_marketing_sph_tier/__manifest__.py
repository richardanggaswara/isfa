# -*- coding: utf-8 -*-
{
    'name': "vit_marketing_sph_tier",

    'summary': """
        Tier validation for marketing sph""",

    'description': """
        Tier validation for marketing sph
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
        'vit_marketing_sph',
        'vit_marketing_sph_inherit', 
        'base_tier_validation',
        'vit_settings_approval',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sph.xml',
        'views/data_tier.xml',

    ],
    
}
