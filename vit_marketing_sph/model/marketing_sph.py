#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _

class marketing_sph(models.Model):

    _name = "vit.marketing_sph"
    _description = "vit.marketing_sph"
    name = fields.Char( required=True, string="Name",  help="")
    sph_no = fields.Char( string="Sph no",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    project = fields.Text( string="Project",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    description = fields.Text( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    revisi = fields.Boolean( string="Revisi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    partner_id = fields.Many2one(comodel_name="res.partner",  string="Partner",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    inquery_id = fields.Many2one(comodel_name="vit.marketing_inquery",  string="Inquery",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rab_id = fields.Many2one(comodel_name="vit.marketing_rab",  string="Rab",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    boq_ids = fields.One2many(comodel_name="vit.boq_sph_line",  inverse_name="sph_id",  string="Boqs",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    term_ids = fields.One2many(comodel_name="vit.term_sph_line",  inverse_name="sph_id",  string="Terms",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    doc_ids = fields.One2many(comodel_name="vit.doc_sph_line",  inverse_name="sph_id",  string="Docs",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
