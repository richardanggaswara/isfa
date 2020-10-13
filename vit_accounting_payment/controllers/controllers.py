# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountingPayment(http.Controller):
#     @http.route('/vit_accounting_payment/vit_accounting_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_accounting_payment/vit_accounting_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_accounting_payment.listing', {
#             'root': '/vit_accounting_payment/vit_accounting_payment',
#             'objects': http.request.env['vit_accounting_payment.vit_accounting_payment'].search([]),
#         })

#     @http.route('/vit_accounting_payment/vit_accounting_payment/objects/<model("vit_accounting_payment.vit_accounting_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_accounting_payment.object', {
#             'object': obj
#         })