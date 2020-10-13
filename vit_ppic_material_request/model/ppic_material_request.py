#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _

class ppic_material_request(models.Model):

    _name = "vit.ppic_material_request"
    _description = "vit.ppic_material_request"
    name = fields.Char( required=True, string="Name",  help="")
    project_des = fields.Text( string="Project", readonly=True, help="")
    product_des = fields.Text( string="Product", readonly=True, help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    note = fields.Text( string="Notes",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    jo_id = fields.Many2one(comodel_name="vit.marketing_jo",  string="JO",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product ID",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    material_request_line_ids = fields.One2many(comodel_name="vit.material_request_line",  inverse_name="material_request_id",  string="Bundle",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
