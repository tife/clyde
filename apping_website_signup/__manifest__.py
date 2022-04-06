# -*- coding: utf-8 -*-

{
    'name': "Website Portal Login",
    'version': '15.0.0.1',
    'summary': '''This module enables approving the users signed up from the Portal and manages signup requests from website.
                signup approve signup verify signup approval.''',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'author': 'Apping Technology',
    'maintainer': 'Apping Technology',
    'website': 'https://appingtechnology.com/',
    'depends': ['website', 'auth_signup'],
    'data': [
        'security/security.xml',
        'data/signup_template_data.xml',
        'data/mail_channel_data.xml',
        'views/template.xml',
        'views/res_config_settings.xml',
        'views/res_users.xml',
        'views/res_partner.xml',
    ],
    'images': ['static/description/icon.jpg',],
    'installable': True,
    'application': False,
    'auto_install': False,
}
