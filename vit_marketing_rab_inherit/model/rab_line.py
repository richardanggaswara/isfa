#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class rab_line(models.Model):
    _name = "vit.rab_line"
    _inherit = "vit.rab_line"

    name = fields.Char( required=False, string="NAME",  help="")
    code = fields.Char( string="CODE",  help="")
    cost = fields.Float( compute="get_total", string="COST",  help="")

    categ_id = fields.Many2one(comodel_name="vit.master_rab_line",  string="Master RAB",  help="")

    
    @api.onchange('categ_id')
    def onchange_inquery(self):
        self.name   = self.categ_id.name
        self.code   = self.categ_id.code

    @api.depends('line_ids')
    def get_total(self):
        for c in self:
            am_total = 0.0
            for co in c.line_ids:
                am_total += co.sub_total
            c.cost = am_total