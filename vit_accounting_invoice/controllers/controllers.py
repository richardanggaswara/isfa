# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountingInvoice(http.Controller):
#     @http.route('/vit_accounting_invoice/vit_accounting_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_accounting_invoice/vit_accounting_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_accounting_invoice.listing', {
#             'root': '/vit_accounting_invoice/vit_accounting_invoice',
#             'objects': http.request.env['vit_accounting_invoice.vit_accounting_invoice'].search([]),
#         })

#     @http.route('/vit_accounting_invoice/vit_accounting_invoice/objects/<model("vit_accounting_invoice.vit_accounting_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_accounting_invoice.object', {
#             'object': obj
#         })