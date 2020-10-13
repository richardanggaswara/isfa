#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _

class marketing_rab(models.Model):

    _name = "vit.marketing_rab"
    _description = "vit.marketing_rab"
    name = fields.Char( required=True, string="Name",  help="")
    project = fields.Text( string="Project",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rab_no = fields.Char( string="Rab no",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_rab = fields.Float( string="Total rab",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    qty = fields.Float( string="Qty",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    satuan = fields.Float( string="Satuan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_price = fields.Float( string="Total price",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    gross = fields.Float( string="Gross",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    note = fields.Text( string="Note",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    due_date = fields.Date( string="Due date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_weight = fields.Float( string="Total weight",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    excepted_gross = fields.Float( string="Excepted gross",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    inquery_id = fields.Many2one(comodel_name="vit.marketing_inquery",  string="Inquery",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    line_ids = fields.One2many(comodel_name="vit.rab_line",  inverse_name="rab_id",  string="Lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rab_product_ids = fields.One2many(comodel_name="vit.rab_product_line",  inverse_name="rab_id",  string="Rab products",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
