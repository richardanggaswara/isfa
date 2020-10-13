#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ppic_material_booking_line(models.Model):

    _name = "vit.ppic_material_booking_line"
    _description = "vit.ppic_material_booking_line"
    name = fields.Char( required=True, string="Name",  help="")
    qty = fields.Float( string="Qty",  help="")


    product_id = fields.Many2one(comodel_name="product.product",  string="Product",  help="")
    booking_id = fields.Many2one(comodel_name="vit.ppic_material_booking",  string="Booking",  help="")
