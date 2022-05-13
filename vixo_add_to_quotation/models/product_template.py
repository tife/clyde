from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_banner_image = fields.Binary(string='Product Banner Image(Top)')
    iframe_url = fields.Char('3D Image Url')
    specification = fields.Html()
    product_details_image = fields.Binary(string='Product Detail Image(Bottom)')
    product_attachment = fields.Binary(string='Specification Sheet')
    product_attachment_dwg = fields.Binary(string='DWG')
    product_attachment_3ds = fields.Binary(string='3DS')
    product_attachment_fbx = fields.Binary(string='FBX')
    dimension = fields.Text()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    customer_note = fields.Text()
    customer_ref = fields.Char()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_name = fields.Char()
