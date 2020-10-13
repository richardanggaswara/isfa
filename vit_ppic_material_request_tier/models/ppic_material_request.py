# -*- coding: utf-8 -*-

from odoo import models

class ppic_material_request(models.Model):
    _name = "vit.ppic_material_request"
    _description = "Material Request(MR)"
    _inherit = ['vit.ppic_material_request', 'tier.validation']
    
    _state_from = ['open']
    _state_to = ['done']