# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class product(models.Model):
	_inherit = 'product.template'

	@api.multi
	def name_get(self):
		return [(template.id, '%s' % (template.name)) for template in self]

class productproduct(models.Model):
	_inherit = 'product.product'

	@api.multi
	def name_get(self):
		return [(product.id, '%s' % (product.product_tmpl_id.name + (format("[" + ', '.join(product.attribute_value_ids.mapped('display_name')) + "]") if product.attribute_value_ids else ""))) for product in self
		]
		