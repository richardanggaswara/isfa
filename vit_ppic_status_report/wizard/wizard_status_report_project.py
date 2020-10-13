from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta

class wizard_project_status_report(models.TransientModel):
	_name = "vit.wizard_project_status_report"

	marketing_jo_id = fields.Many2one(comodel_name="vit.marketing_jo", string="Project No", required=True, store=True)
	project_desc = fields.Text(related="marketing_jo_id.project_name", string="Project Desc", store=True)
	project_owner = fields.Char(related="marketing_jo_id.project_manager", string="Project Owner", store=True)
	customer = fields.Many2one(related="marketing_jo_id.partner_id", string="Customer", store=True)
	contract_no = fields.Many2one(related="marketing_jo_id.po_id", string="Contract No", store=True)
	delivery = fields.Many2one(comodel_name="vit.delivery_jo_line", string="Delivery Sch")
	marketing_lot = fields.Char(string="Marketing Lot")
	marketing_bpm = fields.Float(string="Marketing BPM")
	lot_id = fields.Char(string="Lot ID")
	periode_date_start = fields.Date(string="Periode Start", default=lambda self: time.strftime("%Y-%m-%d"))
	periode_date_end = fields.Date(string="Periode End", default=lambda self: time.strftime("%Y-%m-%d"))
	selection_status = fields.Selection(selection=[('all_date','All'),('date','By Date'),('year','By Year')], string="Selection Periode", default="all_date")

	@api.model
	def year_selection(self):
		year = 2000
		year_list = []
		while year != 2040: # replace 2030 with your end year
			year_list.append((str(year), str(year)))
			year += 1
		return year_list
	
	periode_year = fields.Selection(selection="year_selection",string="Periode Year", default="2019")

	@api.multi
	def get_report(self):
		res = self.env['vit.ppic_schedule'].search([('jo_id','=',self.marketing_jo_id.id)])
		for x in res:
			# z = x.env['vit.schedule_line'].search([('schedule_id','=',res.id)])
			for y in x.schedule_line_ids:
				self.marketing_lot = y.lot
				self.lot_id = y.id
		# ret = self.env['vit.inventory_bpm'].search([('jo_id','=',self.marketing_jo_id.id)])
		# for a in ret:
		# 	b = a.env['vit.bpm_utama_line'].search([('bpm_id','=',ret.id)])
		# 	for c in b:
		# 		self.marketing_bpm = c.weight
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'marketing_jo_name': self.marketing_jo_id.name,
				'marketing_lot': self.marketing_lot,
				'lot_id': self.lot_id,
				'periode_date_start' : self.periode_date_start,
				'periode_date_end' : self.periode_date_end,
				'selection_status' : self.selection_status,
				'periode_year' : self.periode_year,
				'marketing_bpm': self.marketing_bpm,
				'marketing_jo_id': self.marketing_jo_id.id,
				'marketing_tower': self.marketing_jo_id.type_tower,
				'marketing_steel': self.marketing_jo_id.type_steel,
				'marketing_bridge': self.marketing_jo_id.type_bridge,
				'marketing_others': self.marketing_jo_id.type_others,
				'project_desc': self.project_desc,
				'project_owner' : self.project_owner,
				'customer' : self.customer.name,
				'contract_no' : self.contract_no.name,
				'delivery' : self.delivery.delivery_time,
			},
		}

		# use `module_name.report_id` as reference.
		# `report_action()` will call `_get_report_values()` and pass `data` automatically.
		return self.env.ref('vit_ppic_status_report.report_project_status_report').report_action(self, data=data)

class ReportProjectStatus(models.AbstractModel):
	"""Abstract Model for report template.

	for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
	"""

	_name = 'report.vit_ppic_status_report.project_view'

	@api.model
	def _get_report_values(self, docids, data=None):
		marketing_jo_id = data['form']['marketing_jo_id']
		marketing_jo_name = data['form']['marketing_jo_name']
		marketing_tower = data['form']['marketing_tower']
		periode_year = data['form']['periode_year']
		periode_date_start = data['form']['periode_date_start']
		periode_date_end = data['form']['periode_date_end']
		selection_status = data['form']['selection_status']
		marketing_bpm = data['form']['marketing_bpm']
		marketing_lot = data['form']['marketing_lot']
		lot_id = data['form']['lot_id']
		marketing_steel = data['form']['marketing_steel']
		marketing_bridge = data['form']['marketing_bridge']
		marketing_others = data['form']['marketing_others']
		project_desc = data['form']['project_desc']
		project_owner = data['form']['project_owner']
		customer = data['form']['customer']
		contract_no = data['form']['contract_no']
		delivery = data['form']['delivery']

		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'marketing_jo_id': marketing_jo_id,
			'marketing_jo_name': marketing_jo_name,
			'periode_date_start' : periode_date_start,
			'periode_date_end' : periode_date_end,
			'selection_status' : selection_status,
			'marketing_tower' : marketing_tower,
			'marketing_bpm' : marketing_bpm,
			'marketing_steel': marketing_steel,
			'marketing_lot': marketing_lot,
			'periode_year' : periode_year,
			'lot_id' : lot_id,
			'marketing_bridge': marketing_bridge,
			'marketing_others': marketing_others,
			'project_desc': project_desc,
			'project_owner': project_owner,
			'customer': customer,
			'contract_no': contract_no,
			'delivery' : delivery,
		}
