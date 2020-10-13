#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class master_rap_line(models.Model):
    _name = "vit.master_rap_line"
    _inherit = "vit.master_rap_line"

    source  = fields.Selection(selection=[("Product","Product"), ("Account","Account")],  string="Source",  help="")
    relat   = fields.Char(string="Relat")

    @api.onchange('source')
    def _onchange_source(self):
        if self.source == "Product":
            self.relat = "Product"
        else:
            self.relat = "Account"
