#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class product_rap_line(models.Model):

    _name = "vit.product_rap_line"
    _description = "vit.product_rap_line"
    name = fields.Char( required=True, string="Name",  help="")
    weight = fields.Float( string="Weight",  help="")
    qty = fields.Float( string="Qty",  help="")
    satuan = fields.Float( string="Satuan",  help="")
    sub_total = fields.Float( string="Sub total",  help="")
    kode_akun = fields.Char( string="Kode akun",  help="")
    total_weight = fields.Float( string="Total weight",  help="")


    rap_line_id = fields.Many2one(comodel_name="vit.rap_line",  string="Rap line",  help="")
    uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
    product_id = fields.Many2one(comodel_name="product.product",  string="Product",  help="")
    account_id = fields.Many2one(comodel_name="account.account",  string="Account",  help="")
