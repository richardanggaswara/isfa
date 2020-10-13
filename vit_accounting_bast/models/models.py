# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class vit_ppic_bast(models.Model):
	_name = 'vit.ppic_bast'
	_inherit = 'vit.ppic_bast'

	states = fields.Selection([('unposted','Unposted'),('posted','Posted')], string="Status", default="unposted")

	def action_unposted_posted(self):
		self.states = 'posted'

	# def action_posted(self):
	# 	self.states = 'posted'
	
	def action_state_unposted_posted(self):
		obj = []
		currency_name = self.env['res.currency'].search([('name','=','IDR')])
		current_company = self.env['res.company'].browse(self.env['res.company']._company_default_get('vit.ppic_bast'))
		for x in self:
			acc_cred = x.product_id.product_id.property_stock_production.valuation_out_account_id.id
			acc_deb = x.product_id.product_id.categ_id.property_stock_valuation_account_id.id
			if acc_cred and acc_deb:
				obj.append((0, 0, {
					"account_id": acc_cred,
					"partner_id": current_company.id.id,
					"label": self.product_dest,
					"name": x.product_id.name,
					# "amount_currency": x.product_id.standard_price * x.terima_act, 
					"currency_id": currency_name.id,
					"debit": 0,
					"credit": x.product_id.total_price,
					# "tax_ids": x.product_id.taxes_id.id,
					}))
				obj.append((0, 0, {
					"account_id": acc_deb,
					"partner_id": current_company.id.id,
					"label": self.product_dest,
					"name": x.product_id.name,
					# "amount_currency": x.product_id.standard_price * x.terima_act,
					"currency_id": currency_name.id,
					"debit": x.product_id.total_price,
					"credit" : 0,
					# "tax_ids": x.product_id.taxes_id.id,
					}))
			else:
				raise UserError(_('Inventory Stock Valuation(Outgoing) dan Category Stock Valuation pada Product tidak boleh kosong'))
		
		select_cash = self.env['account.journal'].search([('type','=','general'),
			('name','like','Miscellaneous Operations')
			])
		data = {
				"date": datetime.now().strftime('%Y-%m-%d'),
				"ref": self.name,
				"journal_id": select_cash.id,
				"company_id": current_company.id.id,
				"line_ids": obj
				}
		obj_journal = self.env['account.move'].sudo().create(data)
		obj_journal.action_post()
		if self.states == 'unposted':
			self.states = 'posted'