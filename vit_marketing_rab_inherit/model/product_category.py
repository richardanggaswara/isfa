#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class product_category(models.Model):
    _name = "product.category"
    _inherit = "product.category"
