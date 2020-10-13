#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class boq_sph_line(models.Model):
    _name = "vit.boq_sph_line"
    _inherit = "vit.boq_sph_line"

    name                = fields.Char( required=False, string="Name",  help="")
    qty                 = fields.Float( required=True, string="Qty",  help="")
    unit_price          = fields.Float( required=True, string="Unit Price",  help="")
    total               = fields.Float( string="Total Price", compute="_calc_total" , help="")
    unit_weight_sph     = fields.Float( string="Unit Weight (kg)",  help="")
    total_weight_sph    = fields.Float( string="Total Weight (kg)",  help="")

    uom_id              = fields.Many2one( required=True, comodel_name="uom.uom",  string="UOM",  help="")
    product_id          = fields.Many2one( required=True, comodel_name="product.template",  string="Product",  help="")

    @api.depends('qty','unit_weight_sph','unit_price')
    def _calc_total(self):
        for rec in self:
            rec.total = rec.qty * rec.unit_weight_sph * rec.unit_price