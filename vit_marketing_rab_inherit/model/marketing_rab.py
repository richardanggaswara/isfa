#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('done','Done')]

class marketing_rab(models.Model):
    _name = "vit.marketing_rab"
    _inherit = "vit.marketing_rab"
    _order = "date desc"

    name            = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    total_rab       = fields.Float( compute="_calc_total", string="Total RAB", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    qty             = fields.Float( string="Quantity", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    satuan          = fields.Float( compute="_calc_satuan", string="Unit Price/kg", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    total_price     = fields.Float( compute="_calc_total_price", string="Total Propose Price", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    gross           = fields.Float( compute="_calc_gross", string="Expected Gross Margin", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    note            = fields.Text( string="Notes", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    state           = fields.Selection(string='State', default="draft", selection=STATES, readonly=True, states={"draft" : [("readonly",False)]})
    date            = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    partner_id      = fields.Many2one( required=True, comodel_name="res.partner",  string="Customer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    inquery_id      = fields.Many2one(required=True, comodel_name="vit.marketing_inquery",  string="Customer Inquery No", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    due_date        = fields.Date(string="Due Date", states={"draft" : [("readonly",False)]}, help="")
    total_weight    = fields.Float( string="Total weight", compute="_calc_total_weight",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    excepted_gross  = fields.Float(compute="_calc_excepted_gross", string="Margin (%)",  readonly=True, states={"draft" : [("readonly",True)]},  help="")

    @api.depends('total_price','total_weight')
    def _calc_satuan(self):
        for rec in self:
            if rec.total_weight > 0:
                rec.satuan = rec.total_price / rec.total_weight

    @api.depends('gross','total_price')
    def _calc_excepted_gross(self):
        for rec in self:
            if rec.total_price > 0:
                rec.excepted_gross = (rec.gross / rec.total_price) * 100

    @api.depends('total_price','total_rab')
    def _calc_gross(self):
        for rec in self:
            rec.gross = rec.total_price - rec.total_rab

    @api.depends('rab_product_ids','rab_product_ids.total_price' )
    def _calc_total_price(self):
        total_price = 0.0
        for cal in self:
            total_price = 0.0
            for line in cal.rab_product_ids:
                total_price += line.total_price
            cal.total_price = total_price
    
    @api.depends('rab_product_ids','rab_product_ids.total_weight' )
    def _calc_total_weight(self):
        total_weight = 0.0
        for cal in self:
            total_weight = 0.0
            for line in cal.rab_product_ids:
                total_weight += line.total_weight
            cal.total_weight = total_weight

    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_rab') or 'Error Number!!!'
            obj = self.env['vit.master_rab_line'].search([])
            final_data = []
            line_data = []
            # pdb.set_trace()
            vals['line_ids'] = False
            for x in obj:
                line_data = [0, 0, {
                    "categ_id": x.id,
                    "name": x.name,
                    "code": x.code,
                    }]
                final_data.append(line_data)
            vals['line_ids'] = final_data
        return super(marketing_rab, self).create(vals)
    
    @api.onchange('inquery_id')
    def onchange_inquery(self):
        if not self.inquery_id:
            return
        self.partner_id     = self.inquery_id.partner_id
        self.project        = self.inquery_id.project
        self.note           = self.inquery_id.notes
        self.due_date       = self.inquery_id.due_date
        obj = self.env['vit.inquery_line'].search([('inquery_id','=',self.inquery_id.id)])
        line_data = []
        for record in self:
            record.update({"rab_product_ids": False})
            for x in obj:
                line_data = [(0, 0, {
                    "product_id": x.product_id,
                    "qty_product": x.qty,
                    "name": x.product_id.name,
                    "unit_weight": x.weight,
                    })]
                record.update({"rab_product_ids": line_data})
            if record.inquery_id:
                return {'domain':{'rab_id':[('inquery_id', '=',record.inquery_id.id),('state','=','done')]}}

    @api.depends('total_rab','line_ids')
    def _calc_total(self):
        am_total = 0.0
        for c in self:
            for co in c.line_ids:
                am_total += co.cost
                c.total_rab = am_total
    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        if self.total_price == 0:
            raise UserError(_('Product Detail harus terisi !'))
        elif self.total_rab == 0:
            raise UserError(_('Product Detail harus terisi !'))
        else :
            self.state = STATES[1][0]

    @api.multi 
    def action_done(self):
        self.state = STATES[2][0]