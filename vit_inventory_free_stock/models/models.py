# -*- coding: utf-8 -*-

from odoo import models, fields, api

class material_plan_lane_product(models.Model):
	_inherit = "product.product"

	free_stock = fields.Float(string="Free Stock", compute="_compute_free_stock")
	
	def get_free_stock(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Free Stock',
			'view_mode': 'tree',
			'res_model': 'vit.material_plan_lane',
			'domain': [('product_id', '=', self.id)],
			'context': "{'create': False}"
		}

	@api.depends('qty_available')
	def _compute_free_stock(self):
		for record in self:
			available_stock = record.env['stock.quant'].search([('quantity','=',record.qty_available),('product_id','=',record.id),('location_id.complete_name','=','Physical Locations/WH/Stock')])
			# booking = record.env['stock.move.line'].search([('product_id','=',record.id),('location_id.complete_name','=','Physical Locations/WH/Stock')])
			print(available_stock)
			print('==========================================')
			print(record.free_stock)
			record.free_stock = record.qty_available