#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class accounting_tpb(models.Model):

	_name = "vit.accounting_tpb"
	_description = "vit.accounting_tpb"
	name = fields.Char( required=True, string="Name",  help="")
	status = fields.Char( string="Status",  help="")
	date = fields.Date( string="Date",  help="")
	notes = fields.Text( string="Notes",  help="")


	jo_id = fields.Many2one(comodel_name="vit.marketing_jo",  string="Jo",  help="")
	product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product",  help="")
	vendor_id = fields.Many2one(comodel_name="res.partner",  string="Vendor",  help="")
	po_id = fields.Many2one(comodel_name="vit.procurement_po",  string="Po",  help="")
	accounting_tpb_line_ids = fields.One2many(comodel_name="vit.accounting_tpb_line",  inverse_name="accounting_tpb_id",  string="Accounting tpb lines",  help="")
	doc_tpb_ids = fields.One2many(comodel_name="vit.doc_tpb_line",  inverse_name="tpb_id",  string="Doc tpbs",  help="")
