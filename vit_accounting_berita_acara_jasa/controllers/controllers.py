# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountingBeritaAcaraJasa(http.Controller):
#     @http.route('/vit_accounting_berita_acara_jasa/vit_accounting_berita_acara_jasa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_accounting_berita_acara_jasa/vit_accounting_berita_acara_jasa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_accounting_berita_acara_jasa.listing', {
#             'root': '/vit_accounting_berita_acara_jasa/vit_accounting_berita_acara_jasa',
#             'objects': http.request.env['vit_accounting_berita_acara_jasa.vit_accounting_berita_acara_jasa'].search([]),
#         })

#     @http.route('/vit_accounting_berita_acara_jasa/vit_accounting_berita_acara_jasa/objects/<model("vit_accounting_berita_acara_jasa.vit_accounting_berita_acara_jasa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_accounting_berita_acara_jasa.object', {
#             'object': obj
#         })