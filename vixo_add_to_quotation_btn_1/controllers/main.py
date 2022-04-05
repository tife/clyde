# -*- coding: utf-8 -*-
from odoo.http import request, content_disposition
from odoo.tools.translate import _
from odoo import fields, http, SUPERUSER_ID, tools, _
import re
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools.json import scriptsafe as json_scriptsafe
import logging

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json_scriptsafe.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json_scriptsafe.loads(kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        if kw.get('express'):
            return request.redirect("/quotation/download")

        return request.redirect("/shop/cart")

    @http.route(['/quotation/download'], type='http', auth="public", website=True, sitemap=False)
    def donwload_saleorder(self, **kwargs):
        sale_order_id = request.website.sale_get_order(force_create=True)
        if sale_order_id:
            pdf, _ = request.env.ref('vixo_add_to_quotation_btn_1.action_report_saleorder_quotation').with_user(SUPERUSER_ID)._render_qweb_pdf(
                [sale_order_id.id])
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(pdf))]
            filename = "%s.pdf" % (re.sub('\W+', '-', 'Quotation / Order'))
            pdfhttpheaders.append(('Content-Disposition', content_disposition(filename)))
            try:
                template = request.env.ref('sale.email_template_edi_sale', False)
                if template:
                    template.sudo().send_mail(sale_order_id.id, force_send=True, raise_exception=True)
            except:
                _logger.exception('Something went wrong outgoing server')
            return request.make_response(pdf, headers=pdfhttpheaders)
