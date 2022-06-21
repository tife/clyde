from odoo import api, fields, models, _
from odoo.http import request, Controller, route

from odoo.addons.http_routing.models.ir_http import slug


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_banner_image = fields.Binary(string='Product Banner Image(Top)')
    iframe_url = fields.Char('3D Image Url')
    # specification = fields.Html()
    product_details_image = fields.Binary(string='Product Detail Image(Bottom)')
    product_attachment = fields.Binary(string='Specification Sheet')
    product_attachment_dwg = fields.Binary(string='DWG')
    product_attachment_3ds = fields.Binary(string='3DS')
    product_attachment_fbx = fields.Binary(string='FBX')
    dimension = fields.Text()
    materials = fields.Text('Materials')
    dimension_image = fields.Binary(string='Dimension Image')
    care_instructions = fields.Char(string='Care Instructions')
    assembly_instructions = fields.Binary()
    lead_time = fields.Text()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    customer_note = fields.Text()
    customer_ref = fields.Char()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_name = fields.Char()


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    show_in_header = fields.Boolean(string='Show in Header ?')

    @api.model
    def create(self, vals):
        res = super(ProductPublicCategory, self).create(vals)
        website = request.env.company.website_id.get_current_website()
        if res.show_in_header:
            self.env['website.menu'].create({
                'name': res.name,
                'url': '/shop/category/%s' % slug(res),
                'parent_id': website.menu_id.id,
                'website_id': website.id,
                'product_public_category_id': res.id,
            })
        return res

    def write(self, vals):
        res = super(ProductPublicCategory, self).write(vals)
        if vals.get('name'):
            website_menu_id = self.env['website.menu'].search([('product_public_category_id', '=', self.id)], limit=1)
            website_menu_id.name = self.name
        if vals.get('show_in_header'):
            website = request.env.company.website_id.get_current_website()
            if self.show_in_header:
                self.env['website.menu'].create({
                    'name': self.name,
                    'url': '/shop/category/%s' % slug(self),
                    'parent_id': website.menu_id.id,
                    'website_id': website.id,
                    'product_public_category_id': self.id,
                })
        if vals.get('show_in_header') == False:
            website_menu_id = self.env['website.menu'].search([('product_public_category_id', '=', self.id)])
            if website_menu_id:
                website_menu_id.unlink()
        return res


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    product_public_category_id = fields.Many2one('product.public.category')

class Website(models.Model):
    _inherit = "website"

    custom_enquiries = fields.Char('Custom Enquiries')
