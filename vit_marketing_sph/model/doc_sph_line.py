#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class doc_sph_line(models.Model):

    _name = "vit.doc_sph_line"
    _description = "vit.doc_sph_line"
    name = fields.Char( required=True, string="Name",  help="")
    doc = fields.Binary( string="Doc",  help="")
    date = fields.Date( string="Date",  help="")


    sph_id = fields.Many2one(comodel_name="vit.marketing_sph",  string="Sph",  help="")
