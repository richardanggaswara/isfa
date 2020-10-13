#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class master_rab_line(models.Model):
    _name = "vit.master_rab_line"
    _inherit = "vit.master_rab_line"

    name    = fields.Char( required=False, string="Name",  help="")
    source  = fields.Selection(selection=[("Product","Product"), ("Account","Account")],  string="Source",  help="")
    relat   = fields.Char(string="Relat")

    @api.onchange('source')
    def _onchange_source(self):
        if self.source == "Product":
            self.relat = "Product"
        else:
            self.relat = "Account"
    