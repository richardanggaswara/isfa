# -*- coding: utf-8 -*-
from odoo import http

# class VitProductNameGet(http.Controller):
#     @http.route('/vit_product_name_get/vit_product_name_get/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_product_name_get/vit_product_name_get/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_product_name_get.listing', {
#             'root': '/vit_product_name_get/vit_product_name_get',
#             'objects': http.request.env['vit_product_name_get.vit_product_name_get'].search([]),
#         })

#     @http.route('/vit_product_name_get/vit_product_name_get/objects/<model("vit_product_name_get.vit_product_name_get"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_product_name_get.object', {
#             'object': obj
#         })