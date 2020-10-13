#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class material_booking_line(models.Model):

    _name = "vit.material_booking_line"
    _description = "vit.material_booking_line"
    name = fields.Char( required=True, string="Name",  help="")
    date = fields.Date( string="Date",  help="")
    item_mto = fields.Float( string="Item mto",  help="")


    booking_id = fields.Many2one(comodel_name="vit.booking",  string="Booking",  help="")
    material_booking_id = fields.Many2one(comodel_name="vit.material_booking",  string="Material booking",  help="")
