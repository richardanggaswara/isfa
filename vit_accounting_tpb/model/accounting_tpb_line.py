#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class accounting_tpb_line(models.Model):

	_name = "vit.accounting_tpb_line"
	_description = "vit.accounting_tpb_line"
	name = fields.Char( string="Name",  help="")
	qty = fields.Float( string="Qty",  help="")
	total_qty = fields.Float( string="Total qty",  help="")
	code_accounting = fields.Char( string="Code accounting",  help="")
	masuk_act = fields.Float( string="Masuk act",  help="")
	terima_act = fields.Float( string="Terima act",  help="")
	reject_act = fields.Float( string="Reject act",  help="")


	accounting_tpb_id = fields.Many2one(comodel_name="vit.accounting_tpb",  string="Accounting tpb",  help="")
	uom_id = fields.Many2one(comodel_name="uom.uom",  string="Uom",  help="")
	product_id = fields.Many2one(comodel_name="product.product",  string="Product",  help="")
