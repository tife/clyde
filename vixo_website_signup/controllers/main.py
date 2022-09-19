# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class AuthSignupHome(AuthSignupHome):

    @http.route(website=True, auth="public", sitemap=False, csrf=False)
    def web_login(self, *args, **kw):
        """
        Method inherited to show messages if user approved or not.
        And also user may be approved once and again inactivate so,
        Message accordingly.
        """

        response = super(AuthSignupHome, self).web_login(*args, **kw)

        if response.qcontext and response.qcontext.get('login', False):
            inactive_user = request.env['res.users'].sudo().search(
                [('login', '=', response.qcontext.get('login')), ('active', '=', False), ('approved_date', '=', False)])
            if inactive_user:
                response.qcontext.update({'message': _('Clyde is currently reviewing your trade account application.')})
                del response.qcontext['error']
            reinactive_user = request.env['res.users'].sudo().search(
                [('login', '=', response.qcontext.get('login')), ('active', '=', False),
                 ('approved_date', '!=', False)])
            if reinactive_user:
                response.qcontext.update({'message': _('Your login will continue after it approved again..!')})
                del response.qcontext['error']
        return response

    def get_contact_vals(self, company, kw):
        return {
            'company_type': 'person',
            'parent_id': company.id,
        }

    @http.route('/web/signup', type='http', auth='public', website=True, csrf=False)
    def web_auth_signup(self, *args, **kw):
        """
        1) Create structure if company is there then create partner under company.
        2) Check if user need approval or not. if needed then notify users on channel.
        3) Also send emails to all users to approval team.
        """
        response = super(AuthSignupHome, self).web_auth_signup(*args, **kw)
        response.qcontext['states'] = request.env['res.country.state'].sudo().search([])
        response.qcontext['countries'] = request.env['res.country'].sudo().search([])

        if 'error' not in response.qcontext and request.httprequest.method == 'POST':
            company_ids = request.env['res.partner'].sudo().search(
                [('name', '=', kw['company_name']), ('abn', '=', kw['abn']), ('street', '=', kw['street']),
                 ('city', '=', kw['city']), ('state_id', '=', kw['state_id']), ('zip', '=', kw['zip']),
                 ('business_type', '=', kw['business_type']),
                 ])
            company = [company for company in company_ids if company.company_type == 'company']
            if company:
                company = company[0]
            if not company:
                if kw['company_name'] != "":
                    company = request.env['res.partner'].sudo().create({
                        'name': kw['company_name'],
                        'company_type': 'company',
                        'abn': kw['abn'],
                        'entity_name': kw['entity_name'] or False,
                        'street': kw['street'],
                        'city': kw['city'],
                        'state_id': int(kw['state_id']),
                        'country_id': int(kw['country_id']),
                        'zip': kw['zip'],
                        'business_type': kw['business_type'],
                    })
            if kw['company_name'] != "":
                request.env.user.sudo().write({'name': kw['name'] + ' ' + kw['last_name']})
                request.env.user.partner_id.sudo().write(
                    # self.get_contact_vals(company,kw)
                    {'company_type': 'person',
                     'parent_id': company.id,
                     'demo_title': kw['demo_title'],
                     'mobile': kw['mobile'],
                     'phone': kw['phone'],
                     }
                )
            get_param = request.env['ir.config_parameter'].sudo().get_param
            if get_param('auth_signup.signup_approval', 'False').lower() == 'true':
                request.cr.execute(
                    """update res_users set active = 'f',for_approval_menu ='t' where id =%s""" % (request.uid))
                channel_for_approval = request.env.ref('vixo_website_signup.channel_for_approval_users').sudo()
                if channel_for_approval:
                    partners = channel_for_approval.mapped('group_ids').mapped('users').mapped('partner_id')
                    partners_to_add = partners - channel_for_approval.channel_partner_ids
                    if partners_to_add:
                        channel_for_approval.write({'channel_last_seen_partner_ids': [(0, 0, {'partner_id': partner_id})
                                                                                      for partner_id in
                                                                                      partners_to_add.ids]})
                    # channel_for_approval.sudo().message_subscribe(partner_ids=partners.ids)
                    channel_for_approval.sudo().message_post(
                        body=_(
                            "<b>Please review signup request of user %s</b><br/>Find it under Settings -> Users -> To be Approve Users" % (
                            kw['name'])), subject=_('User Approval'),
                        subtype_xmlid='mail.mt_comment', message_type='comment', content_subtype='html')
                template = request.env.ref('vixo_website_signup.mail_template_user_signup_approval',
                                           raise_if_not_found=False)
                if template:
                    template.sudo().with_context(
                        lang=request.env.user.lang,
                        email_to=','.join(channel_for_approval.mapped('group_ids').mapped('users').mapped('email'))
                    ).send_mail(request.env.user.id, force_send=True)
                response = request.render('web.login', {
                    'message': _("Thank you! Clyde is now processing your trade account application. You will receive an email within one business day confirming your account.")})
                response.headers['X-Frame-Options'] = 'DENY'
                request.session.logout(keep_db=True)
        return response

    @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        #qcontext = self.get_auth_signup_qcontext()
        response = super(AuthSignupHome, self).web_auth_reset_password(*args, **kw)
        response.qcontext['states'] = request.env['res.country.state'].sudo().search([])
        response.qcontext['countries'] = request.env['res.country'].sudo().search([])

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return self.web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, _("No login provided.")
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr)
                    request.env['res.users'].sudo().reset_password(login)
                    qcontext['message'] = _("An email has been sent with credentials to reset your password")
            except UserError as e:
                qcontext['error'] = e.args[0]
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)

        response = request.render('auth_signup.reset_password', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

class ResCountryChange(http.Controller):

    @http.route(['/res/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'],
                website=True)
    def country_infos(self, country, **kw):
        states_ids = request.env['res.country.state'].search([('country_id', '=', country.id)])
        return dict(
            states=[(st.id, st.name, st.code) for st in states_ids],
        )
