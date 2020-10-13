#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ppic_material_booking_line(models.Model):
    _name = "vit.ppic_material_booking_line"
    _inherit = "vit.ppic_material_booking_line"

    name = fields.Char( required=False, string="Name",  help="")
    code_material = fields.Char(string="Code",related="product_id.default_code")
    weight = fields.Float(string="Weight")