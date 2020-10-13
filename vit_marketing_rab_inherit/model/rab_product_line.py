#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class rab_product_line(models.Model):

    _name           = "vit.rab_product_line"
    _inherit        = "vit.rab_product_line"
    _description    = "vit.rab_product_line"

    name = fields.Char( required=False, string="Name",  help="")
    qty_product = fields.Float( string="Qty",  help="")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product",  help="")
    unit_weight = fields.Float( string="Unit Weight (kg)",  help="")
    total_weight = fields.Float(compute="_calc_totalweight", string="Total Weight (kg)",  help="")
    unit_price = fields.Float( string="Unit Price",  help="")
    total_price = fields.Float( compute="_calc_totalprice", string="Total Price",  help="")


    rab_id = fields.Many2one(comodel_name="vit.marketing_rab",  string="Rab",  help="")
    uom_id = fields.Many2one(comodel_name="uom.uom",  string="UOM",  help="")
    
    @api.depends('qty_product','unit_weight')
    def _calc_totalweight(self):
        for rec in self:
            rec.total_weight = rec.qty_product * rec.unit_weight

    @api.depends('total_weight','unit_price')
    def _calc_totalprice(self):
        for rec in self:
            rec.total_price = rec.total_weight * rec.unit_price
