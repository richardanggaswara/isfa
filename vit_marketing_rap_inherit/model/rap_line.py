#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class rap_line(models.Model):
    _name = "vit.rap_line"
    _inherit = "vit.rap_line"

    name            = fields.Char( required=False, string="Name",  help="")
    code            = fields.Char( string="Code",  help="")
    cost_rap        = fields.Float( compute="_calc_total", string="Total RAP",  help="")
    cost_rab        = fields.Float(related="rap_id.jo_id.po_id.sph_id.rab_id.total_rab", string="Total RAB",  help="")
    total_weight    = fields.Float( compute="_calc_total_weight", string="Total Weight",  help="")
    master_rap_id   = fields.Many2one(comodel_name="vit.master_rap_line",  string="Master RAP",  help="")
    rel = fields.Char(related="master_rap_id.relat")

    
    @api.depends('product_rap_line_ids')
    def _calc_total(self):
        for c in self:
            am_total = 0.0
            for co in c.product_rap_line_ids:
                am_total += co.sub_total
            c.cost_rap = am_total

    @api.depends('product_rap_line_ids','product_rap_line_ids.total_weight')
    def _calc_total_weight(self):
        am_total = 0.0
        for c in self:
            am_total = 0.0
            for co in c.product_rap_line_ids:
                am_total += co.total_weight
            c.total_weight = am_total

    
    @api.onchange('master_rab_id')
    def onchange_inquery(self):
        self.name   = self.master_rab_id.name
        self.code   = self.master_rab_id.code