
STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _


class wizard_material_plan_all_inherit(models.TransientModel):
	_name = "vit.wizard_material_plan_all_inherit"

	def _get_active_applicant(self):
		context = self.env.context
		if context.get('active_model') == 'vit.material_plan':
			return context.get('active_id', False)
		return False

	material_plan_id = fields.Many2one(comodel_name="vit.material_plan", string="Material Plan", help="", default=_get_active_applicant)
	product_id = fields.Many2one(string="Product ID", comodel_name="vit.product_jo_line",required=True, help="", related="material_plan_id.product_id")
	pr_ids = fields.One2many('vit.pr', 'mp_id', string="Wizard PR lines", related="material_plan_id.pr_ids")
	state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

	def refresh_wizard(self):
		return { 'type' :  'ir.actions.act_close_wizard_and_reload_view' }