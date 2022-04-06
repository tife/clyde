from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_banner_image = fields.Binary(string='Product Banner Image')
    iframe_url = fields.Char('3D Image Url')
