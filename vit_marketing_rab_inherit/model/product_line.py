#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class product_line(models.Model):
    _name = "vit.product_line"
    _inherit = "vit.product_line"

    name        = fields.Char( required=False, string="Name",  help="")
    rel         = fields.Char(related="rab_line_id.categ_id.relat")
    satuan      = fields.Float( string="Price per Item",  help="")
    qty         = fields.Float( string="Quantity",  help="")
    weight      = fields.Float( string="Unit Weight (kg)", default=1, help="")
    uom_id      = fields.Many2one(comodel_name="uom.uom",  string="UOM",  help="")
    tot_weight  = fields.Float( string="Total Weight (kg)", compute="_calc_tot_weight", help="")
    kode_akun   = fields.Char( related="account_id.code", string="Kode akun",  help="")
    sub_total   = fields.Float( string="Total Price", compute="_calc_subtotal", help="")
    product_id  = fields.Many2one( comodel_name="product.template",  string="Pekerjaan/Bahan",  help="")
    account_id  = fields.Many2one(comodel_name="account.account",  string="Kode Akun",  help="")
    satuan_uom  = fields.Float( string="Price per Uom",  help="", compute="_calc_price_uom")
    

    @api.depends('tot_weight','satuan')
    def _calc_subtotal(self):
        for rec in self:
            rec.sub_total = rec.tot_weight * rec.satuan
    
    @api.depends('weight','qty')
    def _calc_tot_weight(self):
        for rec in self:
            rec.tot_weight = rec.weight * rec.qty

    @api.depends('weight','satuan')
    def _calc_price_uom(self):
        for res in self:
            if not res.weight:
                return
            else:
                res.satuan_uom = float(res.satuan / res.weight)
    
    @api.onchange('product_id')
    def _onchange_product(self):
        self.uom_id = self.product_id.uom_id
