# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class vit_accounting_ap_payment(models.Model):
	_name = 'account.payment'
	_inherit = 'account.payment'

	inv_rekanan_no = fields.Char(string="Inv Rekanan No", related="invoice_ids.inv_rekan_no", store=True)
	partner_id = fields.Many2one(string="Partner", readonly=False)
	inv_rekanan_date = fields.Date(string="Inv Rekanan Date", related="invoice_ids.date_due", store=True)
	tpb_id = fields.Many2one(string="TPB Id", related="invoice_ids.tpb_id", store=True)
	tpb_date = fields.Date(string="TPB Date", related="invoice_ids.tpb_date", store=True)
	po_id = fields.Many2one(string="PO Id", related="invoice_ids.tpb_po_id", store=True)
	po_date = fields.Date(string="PO Date", related="invoice_ids.tpb_po_date", store=True)
	tax_line_ids = fields.One2many(string="Tax", related="invoice_ids.tax_line_ids")
	jo_id = fields.Many2one(string="JO Id", related="invoice_ids.tpb_jo_id", store=True)
	jo_project = fields.Text(string="JO Project", related="invoice_ids.tpb_jo_name", store=True)
	vendor_code = fields.Char(string="Vendor Code", related="invoice_ids.reference_vendor", store=True)
	total_po = fields.Float(string="Total Po", related="invoice_ids.total_po", store=True)
	doc_ap_payment_ids = fields.One2many(comodel_name="vit.doc_ap_payment_line", inverse_name="payment_id", string="Doc AP Payment Line")
	ppn = fields.Monetary(string="PPN", compute="_compute_payment_ppn", store=True)
	total = fields.Monetary(string="Total", compute="_compute_payment_ppn", store=True)
	term_payment_ids = fields.Many2one(sring="Terms", related="invoice_ids.payment_term_id", store=True)
	
	@api.onchange('invoice_ids')
	def onchange_ap_payment(self):
		if not self.invoice_ids:
			return
		
		if self.invoice_ids and len(self.invoice_ids) > 1:
			# self.invoice_ids = [(6, 0, self.invoice_ids[0].id)]
			raise UserError("Satu Payment tidak boleh lebih dari satu Invoice ID")

		res = self.env['account.invoice'].search([('id','=',self.invoice_ids.id)])

		self.partner_id = res.partner_id
		self.amount = self.invoice_ids.residual

	@api.depends('amount')
	def _compute_payment_ppn(self):
		for loop in self:
			loop.ppn = loop.amount * 0.1
			loop.total = (loop.amount * 0.1) + loop.amount

class doc_ap_payment_line(models.Model):

	_name = "vit.doc_ap_payment_line"
	_description = "vit.doc_ap_payment_line"

	name = fields.Binary( required=False, string="File", help="")
	data = fields.Char(string="Name")
	date = fields.Datetime( string="Date", help="", default=datetime.today())
	desc = fields.Text( string="Desc", help="")

	payment_id = fields.Many2one(comodel_name="account.payment", string="Payment")