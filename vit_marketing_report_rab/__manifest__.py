# -*- coding: utf-8 -*-
{
    'name': "vit_marketing_report_rab",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "richard.angga51@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_marketing'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/marketing_rab.xml'
    ],
}