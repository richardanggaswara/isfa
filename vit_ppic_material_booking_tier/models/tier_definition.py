from odoo import api, models


class Tierppic_material_booking(models.Model):
    _inherit = "tier.definition"

    @api.model
    def _get_tier_validation_model_names(self):
        res = super(Tierppic_material_booking, self)._get_tier_validation_model_names()
        res.append("vit.ppic_material_booking")
        return res
