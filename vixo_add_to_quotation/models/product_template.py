from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_banner_image = fields.Binary(string='Product Banner Image(Top)')
    iframe_url = fields.Char('3D Image Url')
    specification = fields.Html()
    product_details_image = fields.Binary(string='Product Detail Image(Bottom)')
    product_attachment = fields.Binary(string='Product Attachment')

