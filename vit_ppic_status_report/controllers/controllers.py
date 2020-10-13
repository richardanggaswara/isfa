# -*- coding: utf-8 -*-
from odoo import http

# class VitPpicStatusReport(http.Controller):
#     @http.route('/vit_ppic_status_report/vit_ppic_status_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_ppic_status_report/vit_ppic_status_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_ppic_status_report.listing', {
#             'root': '/vit_ppic_status_report/vit_ppic_status_report',
#             'objects': http.request.env['vit_ppic_status_report.vit_ppic_status_report'].search([]),
#         })

#     @http.route('/vit_ppic_status_report/vit_ppic_status_report/objects/<model("vit_ppic_status_report.vit_ppic_status_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_ppic_status_report.object', {
#             'object': obj
#         })