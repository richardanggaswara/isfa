#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _
import pdb

class wizard_material_booking(models.Model):

	_name = "vit.wizard_material_booking"
	_description = "vit.wizard_material_booking"

	def _get_active_applicant(self):
		context = self.env.context
		if context.get('active_model') == 'vit.material_plan':
			return context.get('active_id', False)
		return False

	material_plan_id = fields.Many2one(comodel_name="vit.material_plan",  string="Material Plan",  help="", default=_get_active_applicant)

	name = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
	date = fields.Date( string="Date",  readonly=True, related="material_plan_id.date",  help="")
	product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product",  readonly=True,  help="", related="material_plan_id.product_id")
	wizard_booking_ids = fields.One2many(comodel_name="vit.wizard_material_booking_line",  inverse_name="wizard_booking_id",  string="Wizard Booking lines", help="")
	wizard_booking_add_line_ids = fields.Many2many(comodel_name="vit.material_plan_lane")
	mp_id = fields.Many2one(comodel_name="vit.material_plan", string="Material Plan", help="")

	
	@api.onchange('material_plan_id','wizard_booking_add_line_ids')
	def onchange_material_booking(self):
		domain = []
		if self.material_plan_id:
			domain.append(('material_plan_id','=', self.material_plan_id.id))
			domain.append(('wh_obj','>',0))
		return {'domain': {'wizard_booking_add_line_ids': domain }}

	# @api.model
	# def _get_material_booking(self):
	# 	if not self.material_plan_id:
	# 		return
	# 	else:
	# 		return self.env['vit.material_plan_lane'].sudo().search([('material_plan_id','=',self.material_plan_id.id),('wh_obj','>',0)])
	# @api.onchange('material_plan_id')
	# def onchange_rab(self):
	# 	if not self.material_plan_id:
	# 		return

	# 	obj = self.env['vit.material_plan_lane'].search([('material_plan_id','=',self.material_plan_id.id)])
	# 	line_data = []
	# 	for record in self:
	# 		record.update({"wizard_booking_ids": False})
	# 		for x in obj:
	# 			if x.wh_obj > 0:
	# 				if x.total_qty > x.wh_obj:
	# 					qty = x.wh_obj
	# 				else:
	# 					qty = x.total_qty
	# 				line_data = [(0, 0, {
	# 					"product_id": x.product_id.id,
	# 					"name_material": x.product_id.name,
	# 					"qty": qty,
	# 					})]
	# 				record.update({"wizard_booking_ids": line_data})

	@api.multi
	def confirm(self, vals):
		# if not vals.get('name', False) or vals['name'] == 'New':
		#     plan = vals.get('material_plan_id')
		wizard_line = self.wizard_booking_add_line_ids
		line = []
		for y in wizard_line:
			line.append((0, 0, {
					"product_id": y.product_id.id,
					"qty": y.qty,
					"weight": y.weight,
					}))
		data = {
				"product_id": self.product_id.id,
				"date": self.date,
				"mp_id": self.material_plan_id.id,
				"material_plan_id": self.material_plan_id.id,
				"booking_line_ids": line
				}
		res = self.env['vit.ppic_material_booking'].create(data)
		return {
				'type': 'ir.actions.client',
				'tag': 'reload',
				}
				
class wizard_material_booking_line(models.Model):
	_name = "vit.wizard_material_booking_line"
	_description = "vit.wizard_material_booking_line"

	wizard_booking_id = fields.Many2one(comodel_name="vit.wizard_material_booking", string="Wizard Booking")
	product_id = fields.Many2one(comodel_name="product.product",  string="Product", help="")
	name = fields.Char( string="Name",  help="", related='product_id.default_code')
	qty = fields.Float( string="Qty",  help="")
	uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
	weight = fields.Float( string="Total Weight",  help="", compute="_compute_weight")
	name_material = fields.Char(string="Product")

	@api.depends("qty")
	def _compute_weight(self):
		for rec in self:
			rec.weight = rec.product_id.weight * rec.qty
