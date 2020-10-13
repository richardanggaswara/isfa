#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class master_rab_line(models.Model):

    _name = "vit.master_rab_line"
    _description = "vit.master_rab_line"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Code",  help="")
    source = fields.Selection(selection=[('product','Product'), ('account','Account')],  string="Source",  help="")


