#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ppic_material_request(models.Model):
	_name = "vit.ppic_material_request"
	_inherit = "vit.ppic_material_request"

	name = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
	jo_id = fields.Many2one(comodel_name="vit.marketing_jo",  string="JO No", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
	product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product ID", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
	mp_id = fields.Many2one(comodel_name="vit.material_plan", string="Import MP No")
	lot_id =fields.Many2one(comodel_name="vit.schedule_line", required=True,string="Lot")
	project_des = fields.Text( string="Project", readonly=True, related="jo_id.project_name", help="")
	product_des = fields.Char( string="Product", readonly=True, related="product_id.product_id.name", help="")
	total_mto = fields.Float(string="QTY MTO", compute="_calc_subtotal")
	state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
	
	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('vit.ppic_material_request') or 'Error Number!!!'
		return super(ppic_material_request, self).create(vals)

	@api.multi
	def action_generate(self):
		line_data = []

		self.env.cr.execute("delete from vit_material_request_line where material_request_id = %s", (self.id, ))
		for line in self.mp_id.material_plan_line_ids:
			if line.book_obj > 0:
				res = self.env['vit.work_order'].search([('code_material','=',line.code_material),('product_id','=',self.product_id.id)])
				for wo in res:
					# enc = self.env['vit.inventory_bpm'].search([('material_request_id','=',self.id),('wo_id','=', wo.id)])
					line_data.append((0,0,{
						"wo_id": wo.id,
						"code": line.code_material,
						"description": line.name,
						"mto":line.book_obj,
						# "bpm_id": enc.id,
					}))
					
		self.material_request_line_ids =  line_data

	# @api.onchange('jo_id')
	# def onchange_partner(self):
	# 	if self.jo_id:
	# 		return {'domain':{'product_id':[('jo_id', '=',self.jo_id.id)]}}

	def action_confirm(self):
		for res in self.material_request_line_ids:
			if not res.nesting:
				raise UserError(_('Nesting tidak boleh bernilai 0!'))
			if not res.mr:
				raise UserError(_('MR tidak boleh bernilai 0!'))
			if res.nesting > res.mto:
				raise UserError(_('Nilai Nesting tidak boleh lebih dari Nilai MTO!'))
			if res.mr > res.mto:
				raise UserError(_('Nilai MR tidak boleh lebih dari Nilai MTO!'))
			else:
				self.state = STATES[1][0]

	def action_done(self):	
		self.state = STATES[2][0]
		for x in self:
			for y in x.material_request_line_ids:
				for z in y.wo_id:
					z.is_mr = True
					for k in z.bundle_wo_ids:
						if k.state == 'scheduled':
							k.state= 'materialrequest'

	def action_draft(self):
		self.state = STATES[0][0]

	@api.depends('total_mto','material_request_line_ids')
	def _calc_subtotal(self):
		for rec in self:
			sub_total = 0.0
			for loop in rec.material_request_line_ids:
				sub_total += loop.mto
			rec.total_mto = sub_total
