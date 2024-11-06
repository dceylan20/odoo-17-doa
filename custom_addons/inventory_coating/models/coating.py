from odoo import fields, models

class ProductCoating(models.Model):
    _name = 'product.coating'
    _description = 'Product Coating'

    name = fields.Char(string="Coating", required=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    coating = fields.Many2one('product.coating', string="Coating")