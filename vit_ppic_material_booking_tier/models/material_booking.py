# -*- coding: utf-8 -*-

from odoo import models

class ppic_material_booking(models.Model):
    _name = "vit.ppic_material_booking"
    _inherit = ['vit.ppic_material_booking', 'tier.validation']
    
    _state_from = ['open']
    _state_to = ['done']