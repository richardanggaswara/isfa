#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class product_line(models.Model):

    _name = "vit.product_line"
    _description = "vit.product_line"
    name = fields.Char( required=True, string="Name",  help="")
    weight = fields.Float( string="Weight",  help="")
    qty = fields.Float( string="Qty",  help="")
    satuan = fields.Float( string="Satuan",  help="")
    sub_total = fields.Float( string="Sub total",  help="")
    kode_akun = fields.Char( string="Kode akun",  help="")


    rab_line_id = fields.Many2one(comodel_name="vit.rab_line",  string="Rab line",  help="")
    uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product",  help="")
    account_id = fields.Many2one(comodel_name="account.account",  string="Account",  help="")
