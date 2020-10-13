#-*- coding: utf-8 -*-

{
	"name": "Vit marketing rap",
	"version": "1.0", 
	"depends": [
		'base','vit_marketing','stock','account','vit_marketing_jo'
		,'vit_enginering_mto'
	],
	"author": "My Company",
	"category": "Utility",
	"website": "richard.angga51@gmail.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Vit marketing rap module generated by StarUML Odoo Generator Pro Version",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/marketing_rap.xml",
		"view/rap_line.xml",
		"view/product_rap_line.xml",
		# "view/uom.xml",
		# "view/product.xml",
		# "view/account.xml",
		# "view/marketing_jo.xml",
		"view/master_rap_line.xml",
		# "report/marketing_rap.xml",
		# "report/rap_line.xml",
		# "report/product_rap_line.xml",
		# "report/uom.xml",
		# "report/product.xml",
		# "report/account.xml",
		# "report/marketing_jo.xml",
		# "report/master_rap_line.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}