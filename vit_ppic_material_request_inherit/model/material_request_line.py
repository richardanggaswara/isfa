#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class material_request_line(models.Model):
	_name = "vit.material_request_line"
	_inherit = "vit.material_request_line"

	wo_id = fields.Many2one(comodel_name="vit.work_order", help="")
	description = fields.Many2one(comodel="product.product", related="wo_id.name_material", string="Description", help="")
	name = fields.Char(string="Name", help="")
	code = fields.Char(string="Code", help="", related="wo_id.code_material")
	status_mr = fields.Boolean(string="Status MR")
	bpm_id = fields.Many2one(comodel_name="vit.inventory_bpm", string="No BPM")
	
	# @api.model
	# def _get_default_name(self):
	# 	res = self.env["vit.inventory_bpm"].search(["material_request_id","=",self.material_request_id])
	# 	return res
	@api.onchange('material_request_id')
	def onchange_material_req_line(self):
		if not self.material_request_id:
			return
		enc = self.env["vit.inventory_bpm"].search([("material_request_id","=",self.material_request_id),("wo_id","=", self.wo_id)])
		self.bpm_id = enc.id
