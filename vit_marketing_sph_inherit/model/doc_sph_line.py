#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
import base64

class doc_sph_line(models.Model):
    _name = "vit.doc_sph_line"
    _inherit = "vit.doc_sph_line"

    name = fields.Char( required=False, string="Description",  help="")
    doc = fields.Binary( string="Document Name",  help="")
    doc_name = fields.Char( string="Document Name",)
    date = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"),  help="")