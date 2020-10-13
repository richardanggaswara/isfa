from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta

class wizard_enginering_status_report(models.TransientModel):
	_name = "vit.wizard_enginering_status_report"

	marketing_jo_id = fields.Many2one(comodel_name="vit.marketing_jo", string="Project No", store=True)
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
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'periode_date_start' : self.periode_date_start,
				'periode_date_end' : self.periode_date_end,
				'selection_status' : self.selection_status,
				'periode_year' : self.periode_year,
				'marketing_jo_id': self.marketing_jo_id.id,
			},
		}

		return self.env.ref('vit_enginering_status_report.enginering_status_report').report_action(self, data=data)

class ReportEngineringStatus(models.AbstractModel):
	"""Abstract Model for report template.

	for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
	"""

	_name = 'report.vit_enginering_status_report.enginering_view'

	@api.model
	def _get_report_values(self, docids, data=None):
		marketing_jo_id = data['form']['marketing_jo_id']
		periode_year = data['form']['periode_year']
		periode_date_start = data['form']['periode_date_start']
		periode_date_end = data['form']['periode_date_end']
		selection_status = data['form']['selection_status']

		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'marketing_jo_id': marketing_jo_id,
			'periode_date_start' : periode_date_start,
			'periode_date_end' : periode_date_end,
			'selection_status' : selection_status,
			'periode_year' : periode_year,
		}
