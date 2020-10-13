# -*- coding: utf-8 -*-
from odoo import http

# class VitInventoryFreeStock(http.Controller):
#     @http.route('/vit_inventory_free_stock/vit_inventory_free_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_inventory_free_stock/vit_inventory_free_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_inventory_free_stock.listing', {
#             'root': '/vit_inventory_free_stock/vit_inventory_free_stock',
#             'objects': http.request.env['vit_inventory_free_stock.vit_inventory_free_stock'].search([]),
#         })

#     @http.route('/vit_inventory_free_stock/vit_inventory_free_stock/objects/<model("vit_inventory_free_stock.vit_inventory_free_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_inventory_free_stock.object', {
#             'object': obj
#         })