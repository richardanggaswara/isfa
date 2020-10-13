#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'), ('open', 'Open'), ('done','Done')]
from odoo import models, fields, api, _

class ppic_material_booking(models.Model):
    _name = "vit.ppic_material_booking"
    _inherit = "vit.ppic_material_booking"

    name = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    product_id = fields.Many2one(comodel_name="vit.product_jo_line",  string="Product",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    booking_line_ids = fields.One2many(comodel_name="vit.ppic_material_booking_line",  inverse_name="booking_id",  string="Booking lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    material_plan_id = fields.Many2one(comodel_name="vit.material_plan", string="Material Plan", help="")

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.ppic_material_booking') or 'Error Number!!!'
        return super(ppic_material_booking, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        for x in self:
            line = []
            location = self.env.ref('stock.stock_location_stock')
            location_dest = self.env.ref('vit_ppic_material_booking_inherit.ppic_material_booking_1')
            picking_type = self.env.ref('stock.picking_type_internal')
            for y in x.booking_line_ids:
                line.append((0, 0, {
                			"name": x.name,
                            "product_id": y.product_id.id,
                            "product_uom_qty": round(y.qty,2),
                            "product_uom": y.product_id.uom_id.id,
                            "location_id": location.id,
                    		"location_dest_id": location_dest.id,
                            }))
            data = []
            data = {
                    "origin": x.name,
                    "location_id": location.id,
                    "location_dest_id": location_dest.id,
                    "picking_type_id": picking_type.id,
                    "move_ids_without_package": line
                    }
            res = self.env['stock.picking'].sudo().create(data)
            res.action_confirm()
            res.action_assign()
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, res.id)]})
            wiz.process()

        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
