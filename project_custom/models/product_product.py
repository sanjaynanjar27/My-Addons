from odoo import api, models, fields


class CustomProduct(models.Model):
    _inherit = 'product.product'

    review_ids = fields.One2many('product.review',inverse_name="product_id",string="Product Reviews")
