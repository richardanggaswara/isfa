# -*- coding: utf-8 -*-

# STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _

class AccountInvoice(models.Model):

	_name = "account.invoice"
	_inherit = "account.invoice"
	
	tpb_id = fields.Many2one(comodel_name="vit.accounting_tpb", string="TPB", help="")
	accounting_tpb_line_ids = fields.One2many(comodel_name="vit.accounting_tpb_line", inverse_name="accounting_apinv_id", string="Accounting AP Lines", help="")
	name_ap = fields.Char(string="Name", readonly=True, default="New")
	inv_rekan_no = fields.Char(string="Inv Rekanan No")
	tpb_id_name = fields.Char(string="TPB No", readonly= True, related="tpb_id.name")
	tpb_date = fields.Date(string="TPB Date", related="tpb_id.date")
	tpb_po_id = fields.Many2one(string="PO No", related="tpb_id.po_id")
	tpb_po_date = fields.Date(string="PO Date", related="tpb_id.po_id.date")
	tpb_jo_id = fields.Many2one(string="Job Order No", related="tpb_id.jo_id")
	tpb_jo_name = fields.Text(related="tpb_id.jo_id.project_name")
	partner_id = fields.Many2one(string="Customer Name", related="tpb_id.vendor_id", store=True)
	# state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
	reference_vendor = fields.Char(string="Vendor Code", related="tpb_id.vendor_id.ref")
	tpb_vendor_id = fields.Many2one(string="Vendor Name", related="tpb_id.vendor_id")
	total_po = fields.Float(string="Total PO", readonly=True, compute="_compute_inv_po")

	doc_ap_ids = fields.One2many(comodel_name="vit.doc_ap_line", inverse_name="tpb_id", string="Doc aps", help="")

	@api.model
	def create(self, vals):
		if not vals.get('name_ap', False) or vals['name_ap'] == 'New':
			nomor = self.env['ir.sequence'].next_by_code('account.invoice') or 'Error Number!!!'
			res =  super(AccountInvoice, self).create(vals)
			nextnumber = res.tpb_id.name
			if nextnumber == False: 
				number = self.name 
			else:
				number = nomor.replace("{{INV}}", nextnumber )
			res.inv_rekan_no = nomor.replace("{{INV}}","")
			res.name_ap = number
			return res

	@api.onchange('tpb_id')
	def onchange_ap_tpb(self):
		if not self.tpb_id:
			return

		line_data = []
		for res in self:
			res.update({"invoice_line_ids": False})
			for loop in self.tpb_id.accounting_tpb_line_ids:
				line_data = [(0,0,{
						"product_id": loop.product_id.id,
						"name": loop.product_id.name,
						"quantity": loop.terima_act,
						"price_unit" : loop.unit_price,
						"account_id": loop.product_id.categ_id.property_stock_account_input_categ_id.id
					})]
				res.update({"invoice_line_ids": line_data})
		
	@api.depends("tpb_id")
	def _compute_inv_po(self):
		for loop in self.tpb_id.accounting_tpb_line_ids:
			self.total_po += loop.terima_act * loop.product_id.standard_price
