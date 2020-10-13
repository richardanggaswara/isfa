#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class rab_product_line(models.Model):

    _name = "vit.rab_product_line"
    _description = "vit.rab_product_line"
    name = fields.Char( required=True, string="Name",  help="")
    qty_product = fields.Float( string="Qty product",  help="")
    unit_weight = fields.Float( string="Unit weight",  help="")
    total_weight = fields.Float( string="Total weight",  help="")
    unit_price = fields.Float( string="Unit price",  help="")
    total_price = fields.Float( string="Total price",  help="")


    rab_id = fields.Many2one(comodel_name="vit.marketing_rab",  string="Rab",  help="")
    uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product",  help="")
