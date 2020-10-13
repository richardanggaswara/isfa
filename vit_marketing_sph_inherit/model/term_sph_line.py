#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class term_sph_line(models.Model):
    _name = "vit.term_sph_line"
    _inherit = "vit.term_sph_line"

    name = fields.Char( required=False, string="Term of Payment",  help="")
    persen = fields.Float( string="%",  help="")
    description_term = fields.Char( string="Description",  help="")