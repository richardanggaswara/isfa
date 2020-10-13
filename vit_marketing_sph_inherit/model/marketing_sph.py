#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
STATES=[('draft', 'Draft'), ('open', 'Open'), ('done','Done')]

class marketing_sph(models.Model):
    _name = "vit.marketing_sph"
    _inherit = "vit.marketing_sph"
    _order = "date desc"

    name        = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    state       = fields.Selection(string='State', default="draft", selection=STATES, readonly=True, states={"draft" : [("readonly",False)]})
    partner_id  = fields.Many2one(required=True, comodel_name="res.partner",  string="Customer", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    inquery_id  = fields.Many2one(required=True, comodel_name="vit.marketing_inquery",  string="Inquery Customer No", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    rab_id      = fields.Many2one(required=True, comodel_name="vit.marketing_rab",  string="RAB No", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    date        = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_sph') or 'Error Number!!!'
        return super(marketing_sph, self).create(vals)

    @api.onchange('rab_id')
    def onchange_rab(self):
        if not self.rab_id:
            return
        self.project        = self.rab_id.project
        self.description    = self.rab_id.note
        obj = self.env['vit.rab_product_line'].search([('rab_id','=',self.rab_id.id)])
        line_data = []
        for record in self:
            record.update({"boq_ids": False})
            for x in obj:
                line_data = [(0, 0, {
                    "product_id": x.product_id,
                    "uom_id" : x.product_id.uom_id,
                    "qty": x.qty_product,
                    "unit_weight_sph": x.unit_weight,
                    "unit_price" : x.unit_price,
                    "total_weight_sph" : x.qty_product * x.unit_weight,
                    "total" : x.total_weight * x.unit_price,
                    })]
                record.update({"boq_ids": line_data})
            if record.inquery_id:
                return {'domain':{'rab_id':[('inquery_id', '=',record.inquery_id.id),('state','=','done')]}}

    @api.onchange('inquery_id')
    def onchange_inquery(self):
        if not self.inquery_id:
            return
        btc = self.env['vit.inquery_doc'].search([('inquery_id','=',self.inquery_id.id)])
        line_data_b = []
        for docu in self:
            docu.update({"doc_ids": False})
            for k in btc:
                line_data_b = [(0, 0, {
                    "name": k.name,
                    "date":k.date,
                    "doc": k.doc,
                    "doc_name": k.doc_name,
                    })]
                docu.update({"doc_ids": line_data_b})

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            return {'domain':{'inquery_id':[('partner_id', '=',self.partner_id.id),('state','=','done')]}}

    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):

        self.state = STATES[1][0]

    @api.multi 
    def action_done(self):
        self.state = STATES[2][0]

    # @api.multi
    # def get_data(self):
    #     record_collection = []
    #     record_collection = self.env['res.partner'].search([('name','ilike','marc')])
    #     print('============================================')
    #     print(record_collection.name)
    #     return record_collection.name