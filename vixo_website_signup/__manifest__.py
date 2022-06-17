# -*- coding: utf-8 -*-

{
    'name': "Website Sign up and Approval",
    'version': '15.0.0.1',
    'summary': '''This module enables approving the users signed up from the Portal and manages sign-up requests from website.
                sign up approve sign up verify signup approval.''',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'author': 'Vixo Digital',
    'maintainer': 'Vixo Digital',
    'website': 'https://vixo-digital.com/',
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
    'assets': {
        'web.assets_frontend': [
            'vixo_website_signup/static/src/js/country_onchange.js',
            'vixo_website_signup/static/src/scss/vixo_website_signup.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
