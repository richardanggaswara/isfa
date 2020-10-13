#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Open'),('done','Done')]
from odoo import models, fields, api, _
import pdb

class wizard_rap(models.Model):

    _name = "vit.wizard_rap"
    _description = "vit.wizard_rap"

    name = fields.Char( string="Name",  help="")
    mto_ids = fields.Many2many(comodel_name="vit.enginering_mto",  string="MTO",  help="")
    jo_id = fields.Many2one(comodel_name="vit.marketing_jo", related="rap_line_id.rap_id.jo_id", string="JO")

    def _get_active_applicant(self):
        context = self.env.context
        if context.get('active_model') == 'vit.rap_line':
            return context.get('active_id', False)
        return False

    rap_line_id = fields.Many2one(comodel_name="vit.rap_line",  string="RAP",  help="", default=_get_active_applicant)
    
    @api.multi 
    def action_import(self):
        for mto in self.mto_ids:
            # self.rap_line_id.update({"product_rap_line_ids": False})
            line_data = []
            for x in mto.material_mto_ids:
                master_rel = self.env['vit.master_rab_rap_rel'].search([('name','ilike',self.rap_line_id.master_rap_id.name)])
                account = self.env['account.account'].search([('select_master_rabrap_rel','=',master_rel.id)])
                line_data = [(0, 0, {
                    "product_id": x.product_id.id,
                    "weight": x.weight_mto,
                    "qty": x.qty_mto,
                    "account_id": account.id,
                    "project_desc": mto.desc_product,
                    "uom_id": x.product_id.uom_id,
                    })]
                self.rap_line_id.update({"product_rap_line_ids": line_data})
