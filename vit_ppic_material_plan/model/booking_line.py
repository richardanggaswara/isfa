#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class booking_line(models.Model):

    _name = "vit.booking_line"
    _description = "vit.booking_line"
    name = fields.Char( required=True, string="Name",  help="")
    qty = fields.Float( string="Qty",  help="")
    weight = fields.Float( string="Weight",  help="")


    booking_id = fields.Many2one(comodel_name="vit.booking",  string="Booking",  help="")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product",  help="")
