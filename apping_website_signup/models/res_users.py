# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from odoo import models, fields, api, _
from datetime import datetime


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    for_approval_menu = fields.Boolean('For Approval Menu', copy=False)
    approved_date = fields.Datetime('Approved Date', copy=False)
    action_by_user_id = fields.Many2one('res.users', string="Approved or Rejected By", copy=False)
    related_mobile = fields.Char(related="partner_id.mobile", string="Mobile.")
    related_phone = fields.Char(related="partner_id.phone", string="Phone.")
    related_partner_id = fields.Many2one(related="partner_id.parent_id")
    related_entity_name = fields.Char(related="related_partner_id.entity_name", string="Entity Name")
    related_abn = fields.Char(related="related_partner_id.abn", string="ABN")
    related_business_type = fields.Selection(related="related_partner_id.business_type", string="Primary Business Type*")
    related_business_name = fields.Char(related="related_partner_id.name",string='Business Name')
    related_street = fields.Char(related="related_partner_id.street",string=' Head office Street Address*')
    related_city = fields.Char(related="related_partner_id.city",string='Suburb')
    related_post_code = fields.Char(related="related_partner_id.city",string='Post Code*')
    related_state = fields.Many2one(related="related_partner_id.state_id",string='Suburb')
    related_country_id = fields.Many2one(related="related_partner_id.country_id",string='Country')

    def approve_user(self):
        self.write({'approved_date':datetime.now(), 'active':True, 'action_by_user_id': self._uid})
        channel_for_approval = self.env.ref('apping_website_signup.channel_for_approval_users')
        channel_for_approval.message_post(
                            body=_("<b>%s User Approved by %s</b>" % (self.name, self.env.user.name)), subject=_('User Approval'),
                            subtype_xmlid='mail.mt_comment', message_type='comment', content_subtype='html')
        self.partner_id.active = True
        template = self.env.ref('apping_website_signup.mail_template_user_signup_account_approved', raise_if_not_found=False)
        if template:
            template.sudo().with_context(
                lang=self.lang,
                auth_login=self.login,
            ).send_mail(self.id, force_send=True)
        
    def reject_user(self):
        self.write({'active':False, 'action_by_user_id': self._uid})
        channel_for_approval = self.env.ref('apping_website_signup.channel_for_approval_users')
        channel_for_approval.message_post(
                            body=_("<b>%s User Rejected by %s</b>" % (self.name, self.env.user.name)), subject=_('User Rejected'),
                            subtype_xmlid='mail.mt_comment', message_type='comment', content_subtype='html')
        self.partner_id.active = False
        template = self.env.ref('apping_website_signup.mail_template_user_signup_account_rejected', raise_if_not_found=False)
        if template:
            template.sudo().with_context(
                lang=self.lang,
                auth_login=self.login,
            ).send_mail(self.id, force_send=True)
