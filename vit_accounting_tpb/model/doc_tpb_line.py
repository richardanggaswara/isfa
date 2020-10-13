#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class doc_tpb_line(models.Model):

	_name = "vit.doc_tpb_line"
	_description = "vit.doc_tpb_line"
	name = fields.Binary( required=True, string="Name",  help="")
	date = fields.Date( string="Date",  help="")
	desc = fields.Text( string="Desc",  help="")


	tpb_id = fields.Many2one(comodel_name="vit.accounting_tpb",  string="Tpb",  help="")
