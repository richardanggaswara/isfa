#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class rab_line(models.Model):

    _name = "vit.rab_line"
    _description = "vit.rab_line"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Code",  help="")
    cost = fields.Float( string="Cost",  help="")


    rab_id = fields.Many2one(comodel_name="vit.marketing_rab",  string="Rab",  help="")
    material_utama_id = fields.Many2one(comodel_name="product.template",  string="Material utama",  help="")
    categ_id = fields.Many2one(comodel_name="vit.master_rab_line",  string="Categ",  help="")
    line_ids = fields.One2many(comodel_name="vit.product_line",  inverse_name="rab_line_id",  string="Lines",  help="")
