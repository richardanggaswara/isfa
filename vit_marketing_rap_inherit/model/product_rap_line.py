#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class product_rap_line(models.Model):
    _name = "vit.product_rap_line"
    _inherit = "vit.product_rap_line"

    name        = fields.Char( required=False, string="Name",  help="", store=True)
    rel         = fields.Char(related="rap_line_id.master_rap_id.relat")
    satuan      = fields.Float( string="Price per Item", help="",compute="_calc_price", store=True)
    qty         = fields.Float( string="Quantity",  help="")
    weight      = fields.Float( string="Weight (kg)",  help="", store=True, readonly=False)
    total_weight= fields.Float( string="Total Weight (kg)", compute="_calc_totweight", store=True)
    sub_total   = fields.Float( string="Total Price", compute="_calc_subtotal", help="", store=True)
    satuan_uom  = fields.Float( string="Price per Kg",  help="", store=True)
    kode_akun   = fields.Char( related="account_id.code", string="Kode akun",  help="", store=True)
    uom_id      = fields.Many2one(comodel_name="uom.uom",  string="UOM",  help="")
    product_id  = fields.Many2one(comodel_name="product.product",  string="Pekerjaan/Bahan",  help="")
    project_desc = fields.Char(string="Project")
    # @api.onchange('product_id')
    # def _onchange_product_weight(self):
    #     self.weight = self.product_id.weight

    @api.depends('qty','weight')
    def _calc_totweight(self):
        for rec in self:
            rec.total_weight = rec.qty * rec.weight

    @api.depends('qty','weight','satuan')
    def _calc_subtotal(self):
        for rec in self:
            rec.sub_total = (rec.qty * rec.weight) * rec.satuan_uom

    @api.depends('weight','satuan_uom')
    def _calc_price(self):
        for res in self:
            if not res.weight:
                return
            else:
                res.satuan = float(res.satuan_uom * res.weight)
    
    @api.onchange('product_id')
    def _onchange_product(self):
        self.uom_id = self.product_id.uom_id
