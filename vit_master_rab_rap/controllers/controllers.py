# -*- coding: utf-8 -*-
from odoo import http

# class VitMasterRabRap(http.Controller):
#     @http.route('/vit_master_rab_rap/vit_master_rab_rap/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_master_rab_rap/vit_master_rab_rap/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_master_rab_rap.listing', {
#             'root': '/vit_master_rab_rap/vit_master_rab_rap',
#             'objects': http.request.env['vit_master_rab_rap.vit_master_rab_rap'].search([]),
#         })

#     @http.route('/vit_master_rab_rap/vit_master_rab_rap/objects/<model("vit_master_rab_rap.vit_master_rab_rap"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_master_rab_rap.object', {
#             'object': obj
#         })