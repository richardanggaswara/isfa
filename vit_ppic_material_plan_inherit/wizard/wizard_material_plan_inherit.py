
STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class wizard_material_plan_inherit(models.TransientModel):
	_name = "vit.wizard_material_plan_inherit"

	material_plan_id = fields.Many2one(comodel_name="vit.material_plan", string="Material Plan", help="")
	name = fields.Char(readonly=True, default='New', string="Name",  help="")
	date = fields.Date( string="Date", related="material_plan_id.date")
	product_id = fields.Many2one(string="Product ID", comodel_name="vit.product_jo_line",required=True, help="", related="material_plan_id.product_id")
	wizard_pr_ids = fields.One2many(comodel_name="vit.wizard_material_plan_pr_line",  inverse_name="wizard_pr_id",  string="Wizard PR lines", help="")
	wizard_pr_add_line_ids = fields.Many2many(comodel_name="vit.material_plan_lane")
	state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

	@api.onchange('material_plan_id','wizard_pr_add_line_ids')
	def onchange_material_booking(self):
		domain = []
		if self.material_plan_id:
			domain.append(('material_plan_id','=', self.material_plan_id.id))
			domain.append(('to_pr','>',0))
		return {'domain': {'wizard_pr_add_line_ids': domain }}

	# @api.onchange('material_plan_id')
	# def onchange_material(self):
	# 	if not self.material_plan_id:
	# 		return
	# 	month = str(self.date.month)
	# 	year = str(self.date.year)
	# 	# self.name = 'ISFA-PR/' + year + '/' + month + '/'
	# 	obj = self.env['vit.material_plan_lane'].search([('material_plan_id','=',self.material_plan_id.id)])
	# 	line_data = []
	# 	for record in self:
	# 		record.update({"wizard_pr_ids": False})
	# 		for x in obj:
	# 			if x.to_pr > 0:
	# 				line_data = [(0, 0, {
	# 					"code_material": x.product_id.default_code,
	# 					"name_material": x.product_id.name,
	# 					"product_id": x.product_id.id,
	# 					"qty": x.to_pr,
	# 					"uom_id": x.uom_id.id,
	# 					})]
	# 				record.update({"wizard_pr_ids": line_data})

	@api.multi
	def confirm(self):
		# plan = self.material_plan_id
		line = []
		for z in self.wizard_pr_add_line_ids:
			line.append((0, 0, {
					"name": z.code_material,
					"product_id": z.product_id.id,
					"qty": z.qty,
					"uom_id": z.uom_id,
					"weight" : z.weight
					}))
		
		data = {
				# "name": self.name,
				'mp_id': self.material_plan_id.id,
				"tipe": "biasa",
				"jo_no":1,
				"jo_id": self.material_plan_id.jo_id.id,
				"project": self.material_plan_id.project_des,
				"date": self.date,
				"pr_line_ids": line,
				"is_show": 1,
				}
		res = self.env['vit.pr'].create(data)
		return {
				'type': 'ir.actions.client',
				'tag': 'reload',
				}
		
class wizard_material_plan_pr_line(models.TransientModel):
	_name = "vit.wizard_material_plan_pr_line"

	wizard_pr_id = fields.Many2one(comodel_name="vit.wizard_material_plan_inherit", string="Wizard Material Plan PR")
	product_id = fields.Many2one(comodel_name="product.product", string="Product", help="")
	code_material = fields.Char( string="Code", help="",)
	qty = fields.Float( string="Qty",  help="")
	weight = fields.Float(string="Total Weight", help="", compute="_compute_weight")
	uom_id = fields.Many2one(comodel_name="uom.uom", string="Uom", help="")
	name_material = fields.Char(string="Product")

	@api.depends("qty")
	def _compute_weight(self):
		for rec in self:
			rec.weight = rec.product_id.weight * rec.qty
