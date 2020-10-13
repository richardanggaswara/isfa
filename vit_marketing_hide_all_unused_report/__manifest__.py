# -*- coding: utf-8 -*-
{
    'name': "vit_marketing_hide_all_unused_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'vit_marketing',
                'vit_marketing_inquery',
                'vit_marketing_sph',
                'vit_marketing_rab',
                'vit_marketing_po',
                'vit_marketing_jo',
                'vit_marketing_rap',
                'vit_enginering_assemblylist',
                'vit_enginering_boltnut',
                'vit_enginering_mto',
                'vit_enginering_partlist',
                'vit_enginering_packing_list',
                'vit_ppic_schedule',],

    # always loaded
    'data': [
        'report/hide_unused_report.xml',
    ],

}