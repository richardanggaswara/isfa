#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class rap_line(models.Model):

    _name = "vit.rap_line"
    _description = "vit.rap_line"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Code",  help="")
    cost_rap = fields.Float( string="Cost rap",  help="")
    cost_rab = fields.Float( string="Cost rab",  help="")
    total_weight = fields.Float( string="Total weight",  help="")


    rap_id = fields.Many2one(comodel_name="vit.marketing_rap",  string="Rap",  help="")
    master_rap_id = fields.Many2one(comodel_name="vit.master_rap_line",  string="Master rap",  help="")
    product_rap_line_ids = fields.One2many(comodel_name="vit.product_rap_line",  inverse_name="rap_line_id",  string="Product rap lines",  help="")
