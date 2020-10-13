# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountingApPayment(http.Controller):
#     @http.route('/vit_accounting_ap_payment/vit_accounting_ap_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_accounting_ap_payment/vit_accounting_ap_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_accounting_ap_payment.listing', {
#             'root': '/vit_accounting_ap_payment/vit_accounting_ap_payment',
#             'objects': http.request.env['vit_accounting_ap_payment.vit_accounting_ap_payment'].search([]),
#         })

#     @http.route('/vit_accounting_ap_payment/vit_accounting_ap_payment/objects/<model("vit_accounting_ap_payment.vit_accounting_ap_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_accounting_ap_payment.object', {
#             'object': obj
#         })