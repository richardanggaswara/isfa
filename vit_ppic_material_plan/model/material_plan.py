#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class material_plan(models.Model):

    _name = "vit.material_plan"
    _description = "vit.material_plan"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")
    qty_lot = fields.Float( string="Qty lot",  help="")
    schedule_start = fields.Date( string="Schedule start",  help="")
    schedule_end = fields.Date( string="Schedule end",  help="")
    date = fields.Date( string="Date",  help="")
    notes = fields.Text( string="Notes",  help="")


    product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product",  help="")
    lot_id = fields.Many2one(comodel_name="vit.schedule_line",  string="Lot",  help="")
    material_plan_line_ids = fields.One2many(comodel_name="vit.material_plan_lane",  inverse_name="material_plan_id",  string="Material plan lines",  help="")
