# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class master_rab_rap_rel(models.Model):
	_name = "vit.master_rab_rap_rel"

	rel_account = fields.Many2one(comodel_name="account.account", string="code", store=True)
	# type_rel = fields.Many2one(string="Type", related="rel_account.user_type_id")
	name = fields.Char( required=True, string="Name",  help="", store=True)
	code = fields.Char( string="Code",  help="", store=True)

class AccountAccount(models.Model):
	_name = "account.account"
	_inherit = "account.account"

	select_master_rabrap_rel = fields.Many2one(comodel_name="vit.master_rab_rap_rel", string="Master RAB/RAP", store=True)	

class rab_line(models.Model):
	_name = "vit.rab_line"
	_inherit = "vit.rab_line"

	select_master_rabrap_rel = fields.Many2one(comodel_name="vit.master_rab_rap_rel", string="Master RAB/RAP", store=True)

	@api.onchange('categ_id')
	def onchange_select_master(self):
		if not self.categ_id:
			return
		master_rel = self.env['vit.master_rab_rap_rel'].search([('name','ilike',self.categ_id.name)])
		self.select_master_rabrap_rel = master_rel.id

class marketing_rab(models.Model):
	_name = "vit.marketing_rab"
	_inherit = "vit.marketing_rab"
	
	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_rab') or 'Error Number!!!'
			obj = self.env['vit.master_rab_line'].search([])
			final_data = []
			line_data = []
			# pdb.set_trace()
			vals['line_ids'] = False
			for x in obj:
				master_rel = self.env['vit.master_rab_rap_rel'].search([('name','ilike',x.name)])
				line_data = [0, 0, {
					"categ_id": x.id,
					"name": x.name,
					"code": x.code,
					"select_master_rabrap_rel": master_rel.id
					}]
				final_data.append(line_data)
			vals['line_ids'] = final_data
		return super(marketing_rab, self).create(vals)

class product_line(models.Model):
	_name = "vit.product_line"
	_inherit = "vit.product_line"

	master_name = fields.Many2one(comodel_name="vit.master_rab_rap_rel", string="RAB", store=True)
	beban = fields.Char(string="Beban")

class rap_line(models.Model):
	_name = "vit.rap_line"
	_inherit = "vit.rap_line"

	select_master_rabrap_rel = fields.Many2one(comodel_name="vit.master_rab_rap_rel", string="Master RAB/RAP", store=True)
	# categ_rap_id = fields.Many2one(comodel_name="vit.master_rap_line",  string="Master rap",  help="")

	@api.onchange('master_rap_id')
	def onchange_select_master(self):
		if not self.master_rap_id:
			return
		master_rel = self.env['vit.master_rab_rap_rel'].search([('name','ilike',self.master_rap_id.name)])
		self.select_master_rabrap_rel = master_rel.id
