#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class material_booking(models.Model):

    _name = "vit.material_booking"
    _description = "vit.material_booking"
    name = fields.Char( required=True, string="Name",  help="")


    material_plan_line_id = fields.Many2one(comodel_name="vit.material_plan_lane",  string="Material plan line",  help="")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product",  help="")
    material_booking_ids = fields.One2many(comodel_name="vit.material_booking_line",  inverse_name="material_booking_id",  string="Material bookings",  help="")
