# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountingApInvoice(http.Controller):
#     @http.route('/vit_accounting_ap_invoice/vit_accounting_ap_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_accounting_ap_invoice/vit_accounting_ap_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_accounting_ap_invoice.listing', {
#             'root': '/vit_accounting_ap_invoice/vit_accounting_ap_invoice',
#             'objects': http.request.env['vit_accounting_ap_invoice.vit_accounting_ap_invoice'].search([]),
#         })

#     @http.route('/vit_accounting_ap_invoice/vit_accounting_ap_invoice/objects/<model("vit_accounting_ap_invoice.vit_accounting_ap_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_accounting_ap_invoice.object', {
#             'object': obj
#         })