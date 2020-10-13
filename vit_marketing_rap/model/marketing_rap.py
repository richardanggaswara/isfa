#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _

class marketing_rap(models.Model):

    _name = "vit.marketing_rap"
    _description = "vit.marketing_rap"
    name = fields.Char( required=True, string="Name",  help="")
    project = fields.Text( string="Project",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    description = fields.Text( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rap_no = fields.Char( string="Rap no",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    po_no = fields.Char( string="Po no",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_rap = fields.Float( string="Total rap",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_weight = fields.Float( string="Total weight",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    harga_satuan = fields.Float( string="Harga satuan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_price = fields.Float( string="Total price",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    gross_margin = fields.Float( string="Gross margin",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    note = fields.Text( string="Note",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    excepted_gross = fields.Float( string="Excepted gross",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    jo_id = fields.Many2one(comodel_name="vit.marketing_jo",  string="Jo",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rap_line_ids = fields.One2many(comodel_name="vit.rap_line",  inverse_name="rap_id",  string="Rap lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
