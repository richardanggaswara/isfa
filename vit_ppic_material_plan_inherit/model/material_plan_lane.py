from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class material_plan_lane(models.Model):
	_name = "vit.material_plan_lane"
	_inherit = "vit.material_plan_lane"

	mto_id = fields.Many2one(comodel_name="vit.enginering_mto", string="Import MTO No")
	book_obj = fields.Float(string="Book", compute="to_compute_book")
	wh_obj = fields.Float(string="WH", related="product_id.qty_available")
	to_pr = fields.Float(string="To PR", compute="to_compute_pr", store=True)
	code_material = fields.Char(string="Code")
	product_tmpl_id = fields.Many2one(comodel_name="product.template")
	wo_id = fields.Many2one(comodel_name="vit.work_order", help="")
	weight = fields.Float( string="Total Weight",  help="", compute="_compute_weight")
	# material_plan_id = fields.Many2one(comodel_name="vit.material_plan", string="Material plan",  help="", store=True)
	# material_plan_line_ids = fields.One2many(comodel_name="vit.material_plan_lane",  inverse_name="material_plan_id",  string="Material plan lines",  help="")

	@api.depends("qty")
	def _compute_weight(self):
		for rec in self:
			rec.weight = rec.product_id.weight * rec.qty

	@api.depends('wh_obj')
	def to_compute_pr(self):
		for loop in self:
			loop.to_pr = loop.total_qty - loop.wh_obj - loop.book_obj
			if loop.to_pr < 0:
				loop.to_pr = 0

	@api.depends('wh_obj')
	def to_compute_book(self):
		for rec in self:
			
			# print('=========================================================')
			# print(rec.material_plan_id.id)
			# self.ensure_one()
			# res = self.env['vit.ppic_material_booking_line'].sudo().search([('product_id','=',rec.product_id.id),('booking_id.material_plan_id','=',rec.material_plan_id.id)]) 
			if rec.material_plan_id :
				sql = """select sum(qty) from vit_ppic_material_booking_line line join vit_ppic_material_booking booking on line.booking_id = booking.id where line.product_id = %s and booking.mp_id = %s and booking.state = 'done' """
						# 
				# res = self.env['vit.material_plan'].search([('id','=', rec.material_plan_id.id)])
				self.env.cr.execute(sql,(rec.product_id.id, rec.material_plan_id.id,))
				_logger.info("-------- material plan %s", rec.material_plan_id.id)
				_logger.info("======== product %s", rec.product_id.id)
			
				# , self.material_plan_id.id))
				result = self.env.cr.fetchone()
				if result :
					rec.book_obj = result[0]
				else :
					rec.book_obj = 0

class material_plan_lane_product(models.Model):
	_inherit = "product.product"

	free_stock = fields.Float(string="Free Stock", compute="_compute_free_stock")
	
	def get_free_stock(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Free Stock',
			'view_mode': 'tree',
			'res_model': 'vit.material_plan_lane',
			'domain': [('product_id', '=', self.id)],
			'context': "{'create': False}"
		}

	@api.depends('qty_available')
	def _compute_free_stock(self):
		for record in self:
			available_stock = record.env['stock.quant'].search([('quantity','=',record.qty_available),('product_id','=',record.id)])
			print(available_stock)
			print('==========================================')
			print(record.free_stock)
			record.free_stock = record.qty_available - (record.qty_available - available_stock.reserved_quantity)
	