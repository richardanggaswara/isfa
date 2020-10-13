from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta

class wizard_ppic_status_report(models.TransientModel):
	_name = "vit.wizard_ppic_status_report"

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
		# res = self.env['vit.inventory_bpm'].search([('jo_id','=',category[0])])
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'periode_date_start': self.periode_date_start,
				'periode_date_end': self.periode_date_end,
				'periode_year' : self.periode_year,
				'selection_status' : self.selection_status,
			},
		}

		# use `module_name.report_id` as reference.
		# `report_action()` will call `_get_report_values()` and pass `data` automatically.
		return self.env.ref('vit_ppic_status_report.report_ppic_status_report').report_action(self, data=data)

class ReportAttendanceRecap(models.AbstractModel):
	"""Abstract Model for report template.

	for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
	"""

	_name = 'report.vit_ppic_status_report.report_ppic_status_view'

	@api.model
	def _get_report_values(self, docids, data=None):
		periode_date_start = data['form']['periode_date_start']
		periode_date_end = data['form']['periode_date_end']
		periode_year = data['form']['periode_year']
		selection_status = data['form']['selection_status']
		
		sql = '''select marketing_jo.id, marketing_jo.name, marketing_jo.date, partner.name, 
					marketing_jo.project_name, marketing_jo.type_tower, marketing_jo.type_steel, 
					marketing_jo.type_bridge, marketing_jo.type_others, marketing_jo.qty, jo_line.weight, 
					jo_line.name, jo_line.jo_id, jo_line.id
					from vit_marketing_jo as marketing_jo 
					join vit_product_jo_line as jo_line on marketing_jo.id = jo_line.jo_id
					join res_partner as partner on partner.id = marketing_jo.partner_id'''
		if selection_status == 'date':
			sql += ''' where marketing_jo.date between '''+"'"+str(periode_date_start)+"'"+''' and '''+"'"+str(periode_date_end)+"'"+''''''
		if selection_status == 'year':
			sql += ''' where date_part('''+"'"+'''year'''+"'"+''', marketing_jo.date) = '''+str(periode_year)+''''''
		sql += ''' group by jo_line.id, marketing_jo.id, partner.id order by marketing_jo.id'''
		self.env.cr.execute(sql) 
		rec = self.env.cr.fetchall()
		for x in rec:
			sql_res = '''select marketing_jo.id, marketing_jo.name, marketing_jo.date, partner.name, 
							marketing_jo.project_name, marketing_jo.type_tower, marketing_jo.type_steel, 
							marketing_jo.type_bridge, marketing_jo.type_others, marketing_jo.qty, marketing_jo.weight 
							from vit_marketing_jo as marketing_jo
							join res_partner as partner on partner.id = marketing_jo.partner_id'''
			if selection_status == 'date':
				sql_res += ''' where marketing_jo.date between '''+"'"+str(periode_date_start)+"'"+''' and '''+"'"+str(periode_date_end)+"'"+''''''
			if selection_status == 'year':
				sql_res += ''' where date_part('''+"'"+'''year'''+"'"+''', marketing_jo.date) = '''+str(periode_year)+''''''
			sql_res += ''' group by marketing_jo.id, partner.id order by marketing_jo.name'''
			self.env.cr.execute(sql_res)
			rest = self.env.cr.fetchall()
		# for record in rec:
		# 	sql_rec = '''select schedule.name, schedule.id, schedule_line.id, schedule_line.qty, schedule_line.lot
		# 				from vit_ppic_schedule as schedule, vit_schedule_line as schedule_line 
		# 				where schedule.jo_id = '''+str(record[0])+''''''
		# 	self.env.cr.execute(sql_rec)
		# 	result = self.env.cr.fetchall()
		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'periode_date_start': periode_date_start,
			'periode_date_end': periode_date_end,
			'selection_status': selection_status,
			'periode_year': periode_year,
			'selection_status': selection_status,
			'docu': rec,
			# 'docum': rest,
			# 'docume': result,
			# 'dox' : result,
		}
