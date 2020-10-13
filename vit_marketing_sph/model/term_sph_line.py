#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class term_sph_line(models.Model):

    _name = "vit.term_sph_line"
    _description = "vit.term_sph_line"
    name = fields.Char( required=True, string="Name",  help="")
    persen = fields.Char( string="Persen",  help="")
    description_term = fields.Char( string="Description term",  help="")


    sph_id = fields.Many2one(comodel_name="vit.marketing_sph",  string="Sph",  help="")
