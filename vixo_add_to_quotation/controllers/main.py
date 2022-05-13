# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, SUPERUSER_ID, _
from odoo import http, fields
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class CustomerPortal(portal.CustomerPortal):

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type,
                                     report_ref='vixo_add_to_quotation.action_report_saleorder_quotation',
                                     download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        # Log only once a day
        if order_sudo:
            # store the date as a string in the session to allow serialization
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_quote_%s' % order_sudo.id] = now
                body = _('Quotation viewed by customer %s', order_sudo.partner_id.name)
                _message_post_helper(
                    "sale.order",
                    order_sudo.id,
                    body,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=order_sudo.user_id.sudo().partner_id.ids,
                )

        values = {
            'sale_order': order_sudo,
            'message': message,
            'token': access_token,
            'landing_route': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order_sudo.partner_id.id,
            'report_type': 'html',
            'action': order_sudo._get_portal_return_action(),
        }
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id

        # Payment values
        if order_sudo.has_to_be_paid():
            logged_in = not request.env.user._is_public()
            acquirers_sudo = request.env['payment.acquirer'].sudo()._get_compatible_acquirers(
                order_sudo.company_id.id,
                order_sudo.partner_id.id,
                currency_id=order_sudo.currency_id.id,
                sale_order_id=order_sudo.id,
            )  # In sudo mode to read the fields of acquirers and partner (if not logged in)
            tokens = request.env['payment.token'].search([
                ('acquirer_id', 'in', acquirers_sudo.ids),
                ('partner_id', '=', order_sudo.partner_id.id)
            ]) if logged_in else request.env['payment.token']
            fees_by_acquirer = {
                acquirer: acquirer._compute_fees(
                    order_sudo.amount_total,
                    order_sudo.currency_id,
                    order_sudo.partner_id.country_id,
                ) for acquirer in acquirers_sudo.filtered('fees_active')
            }
            # Prevent public partner from saving payment methods but force it for logged in partners
            # buying subscription products
            show_tokenize_input = logged_in \
                                  and not request.env['payment.acquirer'].sudo()._is_tokenization_required(
                sale_order_id=order_sudo.id
            )
            values.update({
                'acquirers': acquirers_sudo,
                'tokens': tokens,
                'fees_by_acquirer': fees_by_acquirer,
                'show_tokenize_input': show_tokenize_input,
                'amount': order_sudo.amount_total,
                'currency': order_sudo.pricelist_id.currency_id,
                'partner_id': order_sudo.partner_id.id,
                'access_token': order_sudo.access_token,
                'transaction_route': order_sudo.get_portal_url(suffix='/transaction'),
                'landing_route': order_sudo.get_portal_url(),
            })

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history = request.session.get('my_quotations_history', [])
        else:
            history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, order_sudo))

        return request.render('sale.sale_order_portal_template', values)


class WebsiteSale(http.Controller):

    @http.route(['/update/customer/notes'], type='json', website=True, auth='public', csrf=False)
    def update_customer_notes(self, **post):
        order_line_id = request.env['sale.order.line'].sudo().browse(int(post.get('sale_order_line_id')))
        if order_line_id:
            order_line_id.customer_note = post.get('value')

    @http.route(['/update/customer/ref'], type='json', website=True, auth='public', csrf=False)
    def update_customer_ref(self, **post):
        order_line_id = request.env['sale.order.line'].sudo().browse(int(post.get('sale_order_line_id')))
        if order_line_id:
            order_line_id.customer_ref = post.get('value')

    @http.route(['/update/project/name'], type='json', website=True, auth='public', csrf=False)
    def update_project_name(self, **post):
        order_id = request.env['sale.order'].sudo().browse(int(post.get('sale_order_id')))
        if order_id:
            order_id.project_name = post.get('value')
