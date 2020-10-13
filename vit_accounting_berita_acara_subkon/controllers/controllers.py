# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountingBeritaAcaraSubkon(http.Controller):
#     @http.route('/vit_accounting_berita_acara_subkon/vit_accounting_berita_acara_subkon/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_accounting_berita_acara_subkon/vit_accounting_berita_acara_subkon/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_accounting_berita_acara_subkon.listing', {
#             'root': '/vit_accounting_berita_acara_subkon/vit_accounting_berita_acara_subkon',
#             'objects': http.request.env['vit_accounting_berita_acara_subkon.vit_accounting_berita_acara_subkon'].search([]),
#         })

#     @http.route('/vit_accounting_berita_acara_subkon/vit_accounting_berita_acara_subkon/objects/<model("vit_accounting_berita_acara_subkon.vit_accounting_berita_acara_subkon"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_accounting_berita_acara_subkon.object', {
#             'object': obj
#         })