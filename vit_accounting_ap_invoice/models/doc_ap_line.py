

from odoo import models, fields, api, _
from datetime import datetime

class doc_ap_line(models.Model):

	_name = "vit.doc_ap_line"
	_description = "vit.doc_ap_line"

	name = fields.Binary( required=False, string="File", help="")
	data = fields.Char(string="Name")
	date = fields.Datetime( string="Date", help="", default=datetime.today())
	desc = fields.Text( string="Desc", help="")

	tpb_id = fields.Many2one(comodel_name="account.invoice", string="Tpb", help="")