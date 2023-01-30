# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    demo_title = fields.Selection([
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
    ], string='Title')
    last_name = fields.Char(string='Last Name')
    abn = fields.Char(string='ABN')
    entity_name = fields.Char(string='Entity Name')
    business_type = fields.Selection([
        ('architect', 'Architect'),
        ('furniture_retailer', 'Furniture Retailer'),
        ('interior_designer', 'Interior Designer'),
        ('hospitality', 'Hospitality'),
        ('online_retailer', 'Online Retailer'),
        ('commercial_furniture', 'Commercial Furniture'),
    ], string='Primary Business Type')

