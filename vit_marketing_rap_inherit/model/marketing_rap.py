#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
STATES=[('draft', 'Draft'), ('open', 'Open'), ('done','Done')]

class marketing_rap(models.Model):
    _name = "vit.marketing_rap"
    _inherit = "vit.marketing_rap"
    _order = "date desc"

    name            = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    date            = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"),  help="")
    project         = fields.Text( string="Project Name",)
    description     = fields.Text( string="Project Desc",)
    jo_id           = fields.Many2one(required=True, comodel_name="vit.marketing_jo",  string="Job Order No",  help="")
    total_rap       = fields.Float( compute="_calc_total", string="Total RAP", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    po_no           = fields.Char( string="Po No",  help="", readonly=False, states={"draft" : [("readonly",False)]} )
    partner_id      = fields.Many2one( required=True, comodel_name="res.partner",  string="Customer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    harga_satuan    = fields.Float( compute="_calc_harga_satuan", string="Unit Price", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    total_price     = fields.Float( related="jo_id.total_contract", string="Total Contract Price", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    gross_margin    = fields.Float( compute="_calc_gross", string="Excepted Gross Margin", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    excepted_gross  = fields.Float( compute="_calc_excepted_gross", string="Margin (%)", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    note            = fields.Text( string="Notes",  readonly=True, help="")
    total_weight    = fields.Float( related="jo_id.weight", string="Total Weight",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    doc_line_ids = fields.One2many(comodel_name="vit.document_rap_line",  inverse_name="rap_id",  string="Doc lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_rap') or 'Error Number!!!'
            obj = self.env['vit.master_rap_line'].search([])
            final_data = []
            line_data = []
            # pdb.set_trace()
            vals['rap_line_ids'] = False
            for x in obj:
                master_rel = self.env['vit.master_rab_rap_rel'].search([('name','ilike',x.name)])
                line_data = [0, 0, {
                    "master_rap_id": x.id,
                    "name": x.name,
                    "code": x.code,
                    "select_master_rabrap_rel": master_rel.id
                    }]
                final_data.append(line_data)
            vals['rap_line_ids'] = final_data
        return super(marketing_rap, self).create(vals)

    @api.depends('gross_margin','total_price')
    def _calc_excepted_gross(self):
        for rec in self:
            if rec.total_price > 0:
                rec.excepted_gross = (rec.gross_margin / rec.total_price) * 100

    @api.depends('total_price','total_rap')
    def _calc_gross(self):
        for rec in self:
            rec.gross_margin = rec.total_price - rec.total_rap

    @api.depends('total_rap','total_weight' )
    def _calc_harga_satuan(self):
        for rec in self:
            if rec.total_weight > 0:
                rec.harga_satuan = rec.total_rap / rec.total_weight
    
    @api.onchange('jo_id')
    def onchange_jo(self):
        self.project        = self.jo_id.project_name
        self.description    = self.jo_id.project_desc
        self.po_no          = self.jo_id.po_id.name
        # self.total_price    = self.jo_id.total_contract
        # self.total_weight   = self.jo_id.weight
    
    @api.depends('total_rap','rap_line_ids')
    def _calc_total(self):
        am_total = 0.0
        for c in self:
            for co in c.rap_line_ids:
                am_total += co.cost_rap
                c.total_rap = am_total

    # @api.depends('total_weight','rap_line_ids')
    # def _calc_total_weight(self):
    #     am_total = 0.0
    #     for c in self:
    #         for co in c.rap_line_ids:
    #             am_total += co.total_weight
    #             c.total_weight = am_total
    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):

        self.state = STATES[1][0]

    @api.multi 
    def action_done(self):
        self.state = STATES[2][0]

class document_rap_line(models.Model):
    _name = "vit.document_rap_line"
    
    name = fields.Char( required=False, string="Description",  help="")
    date = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"),  help="")
    doc = fields.Binary( string="Document Name",  help="")
    doc_name = fields.Char( string="Document Name",)

    rap_id = fields.Many2one(comodel_name="vit.marketing_rap",  string="Rap",  help="")
