# -*- coding: utf-8 -*-
{
    'name': "vit_marketing_report_rap",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "richard.angga51@gmail.com",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Report',
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_marketing'],

    # always loaded
    'data': [
       'report/marketing_rap.xml',
    ],
    # only loaded in demonstration mode
}