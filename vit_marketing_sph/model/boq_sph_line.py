#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class boq_sph_line(models.Model):

    _name = "vit.boq_sph_line"
    _description = "vit.boq_sph_line"
    name = fields.Char( required=True, string="Name",  help="")
    qty = fields.Float( string="Qty",  help="")
    unit_price = fields.Float( string="Unit price",  help="")
    total = fields.Float( string="Total",  help="")
    unit_weight_sph = fields.Float( string="Unit weight sph",  help="")
    total_weight_sph = fields.Float( string="Total weight sph",  help="")


    uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
    sph_id = fields.Many2one(comodel_name="vit.marketing_sph",  string="Sph",  help="")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product",  help="")
