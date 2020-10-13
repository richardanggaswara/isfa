# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
STATES = [('draft', 'Draft'), ('open', 'Open'), ('done','Done')]
from datetime import datetime
from odoo.exceptions import UserError

class berita_acara_jasa(models.Model):
	_name = 'vit.accounting_berita_acara_jasa'
	_description = 'vit.accounting_berita_acara_jasa'

	name = fields.Char(string="ID BA jasa", readonly=True, default="New")
	po_id = fields.Many2one(comodel_name="vit.procurement_po", string="PO NO")
	jo_id = fields.Many2one(string="Job Order", related="po_id.jo_id", store=True)
	cost_center = fields.Many2one(comodel_name="vit.cost_center", string="Cost Center", store=True)
	total_po = fields.Float(string="Total PO", related="po_id.total", store=True)
	vendor_id = fields.Many2one(string="Vendor Name", related="po_id.vendor_id", store=True)
	vendor_code = fields.Char(string="Vendor Code", related="vendor_id.ref")
	is_completed = fields.Boolean(string="Completed")
	notes = fields.Text(string="Notes")
	berita_acara_jasa_lines = fields.One2many(comodel_name="vit.accounting_berita_acara_jasa_line",string="Berita Acara jasa Line", inverse_name="berita_acara_jasa_id")
	state = fields.Selection(selection=STATES, readonly=True, default=STATES[0][0], string="State",  help="")
	sisa_progress = fields.Float(string="Sisa", compute="_sisa_compute")
	type_tower = fields.Boolean( string="Tower", related="jo_id.type_tower")
	type_steel = fields.Boolean( string="General Steel Structure", related="jo_id.type_steel")
	type_bridge = fields.Boolean( string="Bridge", related="jo_id.type_bridge")
	type_others = fields.Boolean( string="Others", related="jo_id.type_others")

	@api.onchange('po_id')
	def onchange_po(self):
		if not self.po_id:
			return
		self.cost_center = self.po_id.cost_center_id

	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			nomor = self.env['ir.sequence'].next_by_code('vit.accounting_berita_acara_jasa') or 'Error Number!!!'
			res =  super(berita_acara_jasa, self).create(vals)
			nomor = nomor.replace("{{BA}}",res.po_id.name )
			res.name = nomor 
			return res

	def action_confirm(self):
		self.state = STATES[1][0]

	def action_draft(self):
		self.state = STATES[0][0]

	@api.depends('berita_acara_jasa_lines')
	def _sisa_compute(self):
		for x in self:
			try:
				if len(x.berita_acara_jasa_lines) == 1:
					x.sisa_progress = x.berita_acara_jasa_lines.progress
				else:
					x.sisa_progress = x.berita_acara_jasa_lines[-1].progress - x.berita_acara_jasa_lines[-2].progress
			except:
				pass

	def action_pay(self):
		obj = []
		for rec in max(self.berita_acara_jasa_lines):
			currency_name = self.env['res.currency'].search([('name','=','IDR')])
			# if credit_1 and credit_2 and debet_1 and debet_2:
			if self.type_tower == True or self.type_bridge == True:
				obj.append((0, 0, {
					"account_id": rec.ba_coa_credit_id.id,
					"partner_id": self.vendor_id.id,
					"label": self.vendor_code,
					"name": self.jo_id.name,
					# "amount_currency": x.product_id.standard_price * x.terima_act, 
					"currency_id": currency_name.id,
					"debit": 0,
					"credit": (self.sisa_progress/100) * self.total_po,
					# "tax_ids": x.product_id.taxes_id.id,
					}))
				obj.append((0, 0, {
					"account_id": rec.ba_coa_debit_id.id,
					"partner_id": self.vendor_id.id,
					"label": self.vendor_code,
					"name": self.jo_id.name,
					# "amount_currency": x.product_id.standard_price * x.terima_act,
					"currency_id": currency_name.id,
					"debit": (self.sisa_progress/100) * self.total_po ,
					"credit" : 0,
					# "tax_ids": x.product_id.taxes_id.id,
					}))
				current_company = self.env['res.company'].browse(self.env['res.company']._company_default_get('vit.accounting_berita_acara_jasa'))	
				select_cash = self.env['account.journal'].search([('type','=','cash'),('code','=','CSH1')])
				data = {
						"date": datetime.now().strftime('%Y-%m-%d'),
						"ref": self.name + ", Pekerjaan Jasa",
						"journal_id": select_cash.id,
						"company_id": current_company.id.id,
						"line_ids": obj
						}
				obj_journal = self.env['account.move'].sudo().create(data)
			if self.type_tower == False and self.type_bridge == False:
				raise UserError("Salah satu type antara type tower atau type bridge harus dicentang pada JO")
				# else:
				# 	raise UserError("Stock Input Account(Product Category) dan Stock Valuation Account(Product Category) pada Product tidak boleh kosong")
			
		self.state = STATES[0][0]

	def action_done(self):
		self.state = STATES[2][0]

class berita_acara_jasa_line(models.Model):
	_name = 'vit.accounting_berita_acara_jasa_line'
	_description = 'vit.accounting_berita_acara_jasa_line'

	berita_acara_jasa_id = fields.Many2one(comodel_name="vit.accounting_berita_acara_jasa", string="Berita Acara jasa")
	name = fields.Char(string="No Berita Acara")
	date = fields.Date(string="Date")
	progress = fields.Float(string="Progress(%)", required=True)
	notes = fields.Text(string="Notes")
	diserahkan = fields.Char(string="Diserahkan Oleh")
	diterima = fields.Char(string="Diterima Oleh")
	name_doc = fields.Binary(required=False, string="File", help="")
	data = fields.Char(string="Name")
	date_doc = fields.Date( string="Date",  help="")
	desc_doc = fields.Text( string="Desc",  help="")
	ba_coa_credit_id = fields.Many2one(comodel_name="account.account", string="Account Credit", required=True)
	ba_coa_debit_id = fields.Many2one(comodel_name="account.account", string="Account Debit", required=True)

	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			nomor = self.env['ir.sequence'].next_by_code('vit.accounting_berita_acara_jasa_line') or 'Error Number!!!'
			res =  super(berita_acara_jasa_line, self).create(vals)
			nomor = nomor.replace("{{BALINE}}",str(res.date) )
			res.name = nomor 
			return res
