from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Creating the description field in product.product
    description = fields.Char(
        string='Description',
        help="Description for sales quotation"
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Creating a related field in product.template to mirror the description from product.product
    description = fields.Char(
        related='product_variant_ids.description',  # Relates to the description field in product.product
        string='Description',
        store=True,  # Ensures the value is stored in product.template
        readonly=False,  # Allows modification in product.template as well
        help="Description for the product, linked to the product.product"
    )
