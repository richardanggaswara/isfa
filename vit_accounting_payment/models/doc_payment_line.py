

from odoo import models, fields, api,_
from datetime import datetime

class doc_payment_line(models.Model):

	_name = "vit.doc_payment_line"
	_description = "vit.doc_payment_line"

	name = fields.Binary( required=False, string="File", help="")
	data = fields.Char(string="Name")
	date = fields.Datetime( string="Date", help="", default=datetime.today())
	desc = fields.Text( string="Desc", help="")

	payment_id = fields.Many2one(comodel_name="account.payment", string="Payment", help="")
