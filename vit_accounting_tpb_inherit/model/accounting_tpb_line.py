#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class accounting_tpb_line(models.Model):
	_name = "vit.accounting_tpb_line"
	_inherit = "vit.accounting_tpb_line"

	qty = fields.Float( string="Qty",  help="")
	code_accounting = fields.Char( string="Code accounting",  help="", related="product_id.default_code")
	masuk_act = fields.Float( string="Masuk act",  help="")
	terima_act = fields.Float( string="Terima act", help="", required=True)
	reject_act = fields.Float( string="Reject act",  help="", compute="_compute_reject")
	unit_price = fields.Float(string="Unit Price")
	uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="", related="product_id.uom_id")
	accounting_apinv_id = fields.Many2one(comodel_name="account.invoice",  string="TPB AP Invoice",  help="")
	
	@api.depends('terima_act')
	def _compute_reject(self):
		for x in self:
			if x.terima_act:
				x.reject_act =  x.masuk_act - x.terima_act
			if not x.terima_act:
				x.reject_act = x.masuk_act