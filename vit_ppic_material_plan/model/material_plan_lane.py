#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class material_plan_lane(models.Model):

    _name = "vit.material_plan_lane"
    _description = "vit.material_plan_lane"
    name = fields.Char( required=True, string="Name",  help="")
    qty = fields.Float( string="Qty",  help="")
    total_qty = fields.Float( string="Total qty",  help="")
    book_obj = fields.Float( string="Book",  help="")
    wh_obj = fields.Float( string="Wh",  help="")
    to_pr = fields.Float( string="To pr",  help="")


    material_plan_id = fields.Many2one(comodel_name="vit.material_plan",  string="Material plan",  help="")
    product_id = fields.Many2one(comodel_name="product.product",  string="Product",  help="")
    uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
