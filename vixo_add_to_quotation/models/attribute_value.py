from odoo import api, fields, models, _


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_image = fields.Binary(string='Image')

class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    attr_image = fields.Binary(string='Image',related="product_attribute_value_id.attr_image")
