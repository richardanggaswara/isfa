#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class material_request_line(models.Model):

    _name = "vit.material_request_line"
    _description = "vit.material_request_line"
    name = fields.Char( string="Name", help="")
    code = fields.Char( string="CODE",  help="")
    mto = fields.Float( string="MTO",  help="")
    nesting = fields.Float( string="NESTING",  help="")
    mr = fields.Float( string="MR",  help="")


    material_request_id = fields.Many2one(comodel_name="vit.ppic_material_request",  inverse_name="material_request_line_ids",  string="Material request",  help="")
    wo_id = fields.Many2one(comodel_name="vit.work_order",  string="WO",  help="")
    product_id = fields.Many2one(comodel_name="product.product",  string="Product",  help="")
