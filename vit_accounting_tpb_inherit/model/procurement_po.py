#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class procurement_po(models.Model):
	_name = "vit.procurement_po"
	_inherit = "vit.procurement_po"

	po_id = fields.Many2one(comodel_name="vit.procurement_po",  string="Po",  help="")
	