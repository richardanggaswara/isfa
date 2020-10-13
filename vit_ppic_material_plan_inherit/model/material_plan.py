#!/usr/bin/python
#-*- coding: utf-8 -*-
STATES = [('draft', 'Draft'), ('open', 'Open'), ('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class material_plan(models.Model):
	_name = "vit.material_plan"
	_inherit = "vit.material_plan"

	product_id = fields.Many2one(comodel_name="vit.product_jo_line", string="Product", required=True, help="")
	name = fields.Char(readonly=True, required=True, default='New', string="Name", help="", )
	mto_id = fields.Many2one(comodel_name="vit.enginering_mto", string="Import MTO No")
	lot_id =fields.Many2one(required=True,comodel_name="vit.schedule_line", string="Lot")
	jo_id = fields.Many2one(comodel_name="vit.marketing_jo",  string="JO No", required=True, help="")
	project_des = fields.Text(readonly=True, string="Project", help="", related="jo_id.project_name")
	description = fields.Char(readonly=True, string="Description", help="", related="product_id.product_id.name")
	qty_lot = fields.Float(string="Qty lot", help="", readonly=True, related="lot_id.qty")
	schedule_start = fields.Date( string="Schedule start", help="")
	schedule_end = fields.Date( string="Schedule end", help="")
	state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
	date = fields.Date(required=True, string="Date", help="")
	pr_ids = fields.One2many(comodel_name="vit.pr", inverse_name="mp_id", string="PR")
	booking_ids = fields.One2many(comodel_name="vit.ppic_material_booking", inverse_name="mp_id", string="Booking")
	# @api.multi
	# def action_pr(self):
	# 	line_data = []	
	# 	for lines in self.material_plan_line_ids:
	# 		if lines.to_pr > 0:		
	# 			line_data.append((0,0,{
	# 				"code_material": lines.product_id.id,
	# 				"name": lines.name,
	# 				"qty": lines.qty,
	# 				"product_uom_id": lines.uom_id.id,
	# 				"unit_price" : lines.product_tmpl_id.list_price,
	# 				"product_qty_hand" : lines.wh_obj,
	# 				"product_qty_forecast" : lines.product_id.virtual_available,
	# 				"date_required" : self.schedule_end, 
	# 			}))
			
	# 	if line_data:		
	# 		product_id = self.env['vit.product.request'].create({
	# 			'name': self.name,
	# 			'product_id': self.product_id,
	# 			'pr_date': fields.Date.today(),
	# 			'user_id': self._uid,
	# 			'company_id': self.env.user.company_id.id,
	# 			'date_required' : self.schedule_end,
	# 			'category_id': self.product_id.product_id.categ_id.id,
	# 			'department_id': self.env.user.employee_ids.department_id.id,
	# 			'warehouse_id': self.env.user.employee_ids.department_id.warehouse_id.id,
	# 			'product_request_line_ids': line_data,
	# 		})
	
	@api.multi
	def action_generate(self):
		line_data = []
		self.env.cr.execute("delete from vit_material_plan_lane where material_plan_id = %s", (self.id, ))
		for line in self.mto_id.material_mto_ids:
			line.total_qty = line.qty_mto * self.qty_lot
			line_data.append((0,0,{
				"material_plan_id": self.id,
				"code_material": line.product_id.default_code,
				"name": line.product_id.name,
				"qty": line.qty_mto,
				"total_qty" : line.total_qty,
				"uom_id": line.uom_id,
				"product_id" : line.product_id.id,
				# "product_tmpl_id" : line.product_id.id,
				# "wh_obj": line.product_id.product_tmpl_id.qty_available,
				"mto_id" : self.mto_id  
			}))
		self.material_plan_line_ids = line_data
	
	# @api.multi
	# def close_shift(self):
	# 	name = _('Close Shift')
	# 	view_mode = 'form'			
	# 	return {
	# 		'name': name,
	# 		'view_type': 'form',
	# 		'view_mode': view_mode,
	# 		'res_model': 'vit.enginering_mto',
	# 		'res_id':self.mto_id.id,
	# 		'type': 'ir.actions.act_window',
	# 		'target':'current'
	# 	}
	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('vit.material_plan') or 'Error Number!!!'
		return super(material_plan, self).create(vals)
	

	def action_confirm(self):
		self.state = STATES[1][0]

	def action_done(self):
		self.state = STATES[2][0]

	def action_draft(self):
		self.state = STATES[0][0]