# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class vit_accounting_payment(models.Model):
	_name= "account.payment"
	_inherit= "account.payment"

	invoice_id = fields.Many2one(comodel_name="account.invoice", string="Invoice Id")
	partner_id = fields.Many2one(string="Partner", readonly=False)
	po_id = fields.Many2one(string="Po Id", related="invoice_ids.po_id", store=True)
	po_date = fields.Date(string="Po Date", related="po_id.po_date", store=True)
	jo_id = fields.Many2one(string="Jo Id", related="invoice_ids.jo_id", store=True)
	jo_project = fields.Text(string="Jo project", related="invoice_ids.project", store=True)
	vendor_code = fields.Char(string="vendor code", related="invoice_ids.customer_code", store=True)
	ppn = fields.Monetary(string="PPN", compute="_compute_payment_ppn", store=True)
	total = fields.Monetary(string="Total", compute="_compute_payment_ppn", store=True)
	term_payment_ids = fields.Many2many(comodel_name="account.payment.term",string="Term payment")
	total_po = fields.Float(string="Total Po", related="po_id.total", store=True)
	# amount = fields.Monetary(string='Payment Amount', required=True)
	doc_payment_ids = fields.One2many(comodel_name="vit.doc_payment_line", inverse_name="payment_id", string="Doc payment", help="")

	def action_validate_invoice_payment(self):
		rec = super(vit_accounting_payment, self).action_validate_invoice_payment()
		self.invoice_id = self.invoice_ids.id
		
		_logger.info("========================== rec %s", self.invoice_id)

		return rec

	@api.onchange('invoice_ids')
	def onchange_material(self):
		if not self.invoice_ids:
			return
		
		if self.invoice_ids and len(self.invoice_ids) > 1:
			# self.invoice_ids = [(6, 0, self.invoice_ids[0].id)]
			raise UserError("Satu Payment tidak boleh lebih dari satu Invoice ID")

		res = self.env['account.invoice'].sudo().search([('id','=',self.invoice_ids.id)])

		self.partner_id = res.partner_id
		self.amount = self.invoice_ids.residual
		# self.invoice_id = res.id
		
	@api.depends('amount')
	def _compute_payment_ppn(self):
		for loop in self:
			loop.ppn = loop.amount * 0.1
			loop.total = (loop.amount * 0.1) + loop.amount