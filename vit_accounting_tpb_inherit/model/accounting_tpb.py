#!/usr/bin/python
#-*- coding: utf-8 -*-
STATES = [('draft', 'Draft'), ('open', 'Open'), ('done','Done')]
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class accounting_tpb(models.Model):
	_name = "vit.accounting_tpb"
	_inherit = "vit.accounting_tpb"

	code_vendor = fields.Char(string="Vendor Code", related="vendor_id.ref")    
	po_id = fields.Many2one(comodel_name="vit.procurement_po",  string="Po", help="", required=True, store=True)
	name = fields.Char(string="Name",  help="", readonly=True, default="New")
	vendor_id = fields.Many2one(comodel_name="res.partner",  string="Vendor", help="", related="po_id.vendor_id", store=True)
	jo_id = fields.Many2one(comodel_name="vit.marketing_jo",  string="Jo",  help="", related="po_id.jo_id", store=True)
	customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", default=lambda self: self._get_default_id_company())
	state = fields.Selection(selection=STATES, readonly=True, default=STATES[0][0], string="State",  help="")  
	is_qc_tpb = fields.Boolean( string="QC TPB", help="")
	is_qc_tpb_valid = fields.Boolean( string="QC", help="")
	proj_name = fields.Text(string="Project Name", related="jo_id.project_name")
	surat_jalan = fields.Char(string="Surat Jalan", store=True)
	date_srt_jalan = fields.Date(string="Date Surat Jalan", store=True)
	warehouse = fields.Many2one(comodel_name="stock.warehouse", string="Warehouse", store=True)

	def _get_default_id_company(self):
		return self.env['res.partner'].search([('id','=',1)], limit=1).id

	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			nomor = self.env['ir.sequence'].next_by_code('vit.accounting_tpb') or 'Error Number!!!'
			res =  super(accounting_tpb, self).create(vals)
			nomor = nomor.replace("{{JO}}",res.jo_id.name )
			res.name = nomor 
			return res
	 
	@api.onchange('po_id')
	def onchange_material_po(self):
		if not self.po_id:
			return
		line_data = []
		for res in self:
			res.update({"accounting_tpb_line_ids": False})
			for line in self.po_id.procurement_po_line_ids:
					line_data.append((0,0,{
						"qty": line.qty,
						"code_accounting": line.code_material,
						"uom_id": line.uom_id.id,
						"product_id" : line.product_id.id, 
						"masuk_act" : line.qty,
						"unit_price" : line.unit_price 
					}))
			res.accounting_tpb_line_ids = line_data
		
	
	def action_confirm(self):
		line = []
		for y in self.accounting_tpb_line_ids:
			# if not y.terima_act:
			# 	raise UserError("Stock Input Account(Product Category) dan Stock Valuation Account(Product Category) pada Product tidak boleh kosong")
				# y.reject_act = y.masuk_act
			line.append((0, 0, {
						"product_id": y.product_id.id,
						"product_uom_qty": y.terima_act,
						"name": '%s' % (y.product_id.product_tmpl_id.name + (format("[" + ', '.join(y.product_id.attribute_value_ids.mapped('display_name')) + "]") if y.product_id.attribute_value_ids else "")),
						"product_uom": y.uom_id.id,
						}))
		data = []
		picking_type = self.env['stock.picking.type'].search([('barcode','=','WH-RECEIPTS')])
		display_location = self.env['stock.location'].search([('complete_name','=','Partner Locations/Vendors')])
		data = {
				"partner_id" : self.vendor_id.id,
				"picking_type_id": picking_type.id,
				"location_id": display_location.id,
				"location_dest_id" : picking_type.default_location_dest_id.id,
				"origin" : self.name,
				"move_ids_without_package": line
				}
		res = self.env['stock.picking'].sudo().create(data)
		res.action_confirm()
		res.action_assign()
		act = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, res.id)]})
		act.process()
		obj = []
		currency_name = self.env['res.currency'].search([('name','=','IDR')])
		for x in self.accounting_tpb_line_ids:
			acc_cred = x.product_id.categ_id.property_stock_account_input_categ_id.id
			acc_deb = x.product_id.categ_id.property_stock_valuation_account_id.id
			if acc_cred and acc_deb: 
				obj.append((0, 0, {
					"account_id": acc_cred,
					"partner_id": self.vendor_id.id,
					"label": self.code_vendor,
					"name": '%s' % (x.product_id.product_tmpl_id.name + (format("[" + ', '.join(x.product_id.attribute_value_ids.mapped('display_name')) + "]") if x.product_id.attribute_value_ids else "")),
					# "amount_currency": x.product_id.standard_price * x.terima_act, 
					"currency_id": currency_name.id,
					"debit": 0,
					"credit": x.unit_price * x.terima_act,
					# "tax_ids": x.product_id.taxes_id.id,
					}))
				obj.append((0, 0, {
					"account_id": acc_deb,
					"partner_id": self.vendor_id.id,
					"label": self.code_vendor,
					"name": '%s' % (x.product_id.product_tmpl_id.name + (format("[" + ', '.join(x.product_id.attribute_value_ids.mapped('display_name')) + "]") if x.product_id.attribute_value_ids else "")),
					# "amount_currency": x.product_id.standard_price * x.terima_act,
					"currency_id": currency_name.id,
					"debit": x.unit_price * x.terima_act,
					"credit" : 0,
					# "tax_ids": x.product_id.taxes_id.id,
					}))
				prod_obj = self.env['product.product'].search([('id', '=', x.product_id.id)])
				if prod_obj.qty_available > 0.0:
					price_average = (((prod_obj.qty_available- x.terima_act) * prod_obj.standard_price) + (x.terima_act * x.unit_price))/prod_obj.qty_available
				if prod_obj.qty_available <= 0.0:
					price_average = x.unit_price
				prod_value = {'list_price': 0, 'standard_price': price_average}
				prod_obj.write(prod_value)
			else:
				raise UserError("Stock Input Account(Product Category) dan Stock Valuation Account(Product Category) pada Product tidak boleh kosong")
		current_company = self.env['res.company'].browse(self.env['res.company']._company_default_get('vit.accounting_tpb'))	
		select_cash = self.env['account.journal'].search([('type','=','cash'),('code','=','CSH1')])
		data = {
				"date": datetime.now().strftime('%Y-%m-%d'),
				"ref": self.name,
				"journal_id": select_cash.id,
				"company_id": current_company.id.id,
				"line_ids": obj
				}
		obj_journal = self.env['account.move'].sudo().create(data)

		self.state = STATES[1][0]
		return {
			'name': _('Products'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'product.product',
			# 'type': 'ir.actions.act_window',
			'res_id': prod_obj.id,
			'context': self.env.context
		}

	def action_draft(self):
		self.state = STATES[0][0]

	def action_done(self):
		self.state = STATES[2][0]
		self.is_qc_tpb = True
		self.is_qc_tpb_valid = True
