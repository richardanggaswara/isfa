from odoo import models, fields, api,_
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class vit_accounting_invoice(models.Model):
	_name = 'account.invoice'
	_inherit = 'account.invoice'

	# name_inv = fields.Char(string="Name", readonly=True, default="New")
	bast_id = fields.Many2one(comodel_name="vit.ppic_bast", string="BAST No")
	jo_id = fields.Many2one(string="Job Order No", related="bast_id.jo_id")
	project = fields.Text(string="Project", related="bast_id.project_dest")
	po_id = fields.Many2one(string="PO No", related="jo_id.po_id")
	partner_id = fields.Many2one(string="Customer Name", related="jo_id.partner_id", store=True)
	# partner_id = fields.Many2one('res.partner', string='Partner', change_default=True, states={'draft': [('readonly', False)]}, track_visibility='always', ondelete='restrict', help="You can find a contact by its Name, TIN, Email or Internal Reference.", )
	customer_code = fields.Char(string="Customer No", related="partner_id.ref")
	delivery_address = fields.Text(string="Address", store=True)
	transfer_rek = fields.Text(string="Transfer to")
	

	@api.onchange('partner_id')
	def _get_partner_address(self):
		if not self.partner_id:
			return
		self.delivery_address = "{name} {city}, {state}, {country}\nP.O Box : {zip}\nTel. : {phone}\nEmail : {email}".format(
			name = self.partner_id.street,
			zip= self.partner_id.zip,
			city= self.partner_id.city,
			state= self.partner_id.state_id.name,
			phone= self.partner_id.phone,
			country= self.partner_id.country_id.name,
			email= self.partner_id.email
			)

	@api.onchange('bast_id')
	def change_lines_invoice(self):
		if not self.bast_id:
			return
		line_data = []
		for res in self:
			res.update({"invoice_line_ids": False})
			for que in res.jo_id.product_ids:
				res_que = que.product_id.categ_id.property_stock_account_input_categ_id.id
				product_id_marketing = self.env['product.product'].search([('product_tmpl_id','=',que.product_id.id)])
				if res_que:	
					line_data = [(0,0,{
							"product_id": product_id_marketing.id,
							"name": que.product_id.name,
							"quantity": round(que.total_weight,1),
							"price_unit" : que.unit_price,
							"account_id": res_que,
							# 'invoice_line_tax_ids': self.invoice_line_tax_ids.ids
						})]
					res.update({"invoice_line_ids": line_data})
				else:
					raise UserError(_('Category Stock Valuation pada Product tidak boleh kosong'))
			for loop in res.jo_id.additional_po_ids:
				res_additional = self.env['account.account'].search([('name','like','Persediaan Lainnya')])
				if res_additional:
					line_data = [(0,0,{
							# "product_id": que.product_id.id,
							"name": loop.name,
							"quantity": 1,
							"price_unit" : loop.total_price,
							"account_id": res_additional.id
						})]
					res.update({"invoice_line_ids": line_data})
				else:
					raise UserError(_('Chart of Account pada Product tidak memiliki kategori Persediaan Lainnya'))

class AccountInvoiceLine(models.Model):
	_name = "account.invoice.line"
	_inherit = "account.invoice.line"

	invoice_line_tax_ids = fields.Many2many('account.tax', string='Taxes')
