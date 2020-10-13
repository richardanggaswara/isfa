# -*- coding: utf-8 -*-

from odoo import models

class Sph(models.Model):
    _name = "vit.marketing_sph"
    _description = "Surat Penawaran Harga(SPH)"
    _inherit = ['vit.marketing_sph', 'tier.validation']
    
    _state_from = ['open']
    _state_to = ['done']