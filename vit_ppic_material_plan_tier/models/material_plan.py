# -*- coding: utf-8 -*-

from odoo import models

class material_plan(models.Model):
	_name = "vit.material_plan"
	_description = "Material Planning"
	_inherit = ['vit.material_plan', 'tier.validation']
	
	_state_from = ['open']
	_state_to = ['done']