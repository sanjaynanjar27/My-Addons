from odoo import api, models, fields

class Product(models.Model):
    _name = 'product.review'

    product_id = fields.Many2one('product.product', string="Product")
    ratings = models.Selection([('1','One'),('2','Two'),('3','Three'),('4','Four'),('5','Five')], string="Review")
    description = fields.Char(string="Description")