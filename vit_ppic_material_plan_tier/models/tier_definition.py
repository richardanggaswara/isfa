from odoo import api, models


class Tiermaterial_plan(models.Model):
	_inherit = "tier.definition"

	@api.model
	def _get_tier_validation_model_names(self):
		res = super(Tiermaterial_plan, self)._get_tier_validation_model_names()
		res.append("vit.material_plan")
		return res
