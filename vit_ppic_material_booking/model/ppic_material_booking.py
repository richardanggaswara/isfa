#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'), ('open', 'Open'), ('done','Done')]
from odoo import models, fields, api, _

class ppic_material_booking(models.Model):

    _name = "vit.ppic_material_booking"
    _description = "vit.ppic_material_booking"
    name = fields.Char( required=True, string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    mp_id = fields.Many2one(comodel_name="vit.material_plan", string="Material Plan", help="")
    product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    booking_line_ids = fields.One2many(comodel_name="vit.ppic_material_booking_line",  inverse_name="booking_id",  string="Booking lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
