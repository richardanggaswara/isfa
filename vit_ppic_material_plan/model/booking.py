#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class booking(models.Model):

    _name = "vit.booking"
    _description = "vit.booking"
    name = fields.Char( required=True, string="Name",  help="")
    date = fields.Date( string="Date",  help="")


    booking_line_ids = fields.One2many(comodel_name="vit.booking_line",  inverse_name="booking_id",  string="Booking lines",  help="")
