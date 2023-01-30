import logging
from ast import literal_eval
from collections import OrderedDict
from lxml import etree, html
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, MissingError
from odoo.http import request, Controller, route
from odoo.osv import expression
from random import randint

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.models.website_snippet_filter import WebsiteSnippetFilter


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
    without_login_price = fields.Float()


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


class WebsiteSnippetFilterInherit(WebsiteSnippetFilter):
    _inherit = 'website.snippet.filter'


    def _filter_records_to_values(self, records, is_sample=False):
        res_products = super(WebsiteSnippetFilter, self)._filter_records_to_values(records,is_sample)
        if self.model_name == 'product.product':
            for res_product in res_products:
                product = res_product.get('_record')
                if not is_sample:
                    res_product.update(product.product_variant_id._get_combination_info_variant())
                    if records.env.context.get('add2cart_rerender'):
                        res_product['_add2cart_rerender'] = True
        return res_products

class WebsiteSnippetFilterNew(models.Model):
    _inherit = 'website.snippet.filter'


    def _prepare_values(self, limit=None, search_domain=None):
        """Gets the data and returns it the right format for render."""
        self.ensure_one()

        limit = limit and min(limit, self.limit) or self.limit
        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()
            if 'website_id' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, self.env['website'].get_current_website().website_domain()])
            if 'is_published' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, [('is_published', '=', True)]])
            if search_domain:
                domain = expression.AND([domain, search_domain])
            try:
                if filter_sudo.model_id == 'product.product':
                    records = self.env['product.template'].with_context(**literal_eval(filter_sudo.context)).search(
                        domain,
                        order=','.join(literal_eval(filter_sudo.sort)) or None,
                        limit=limit
                    )
                    return self._filter_records_to_values(records)
                else:
                    records = self.env[filter_sudo.model_id].with_context(**literal_eval(filter_sudo.context)).search(
                        domain,
                        order=','.join(literal_eval(filter_sudo.sort)) or None,
                        limit=limit
                    )
                    return self._filter_records_to_values(records)
            except MissingError:
                _logger.warning("The provided domain %s in 'ir.filters' generated a MissingError in '%s'", domain,
                                self._name)
                return []
        elif self.action_server_id:
            try:
                return self.action_server_id.with_context(
                    dynamic_filter=self,
                    limit=limit,
                    search_domain=search_domain,
                ).sudo().run() or []
            except MissingError:
                _logger.warning("The provided domain %s in 'ir.actions.server' generated a MissingError in '%s'",
                                search_domain, self._name)
                return []