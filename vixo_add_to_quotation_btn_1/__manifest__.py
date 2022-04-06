{
    'name': 'Clyde Custom',
    'category': 'Website/eCommerce',
    'summary': 'clyde custom.',
    'description': 'clyde custom.',
    'version': '15.0.1.0.2',
    'author': 'Akshar Zalavadiya',
    'data': [
        'views/product_template.xml',
        'views/product_template_views.xml',
        'views/attribute_value_views.xml',
        'report/sale_report.xml',
        'report/sale_report_template.xml',
    ],
    'depends': [
        'website_sale',
        'sale_management',
    ],
    'assets': {
        'web.report_assets_common': [
            'vixo_add_to_quotation_btn_1/static/src/scss/sale_report.scss',
        ],
        'web.assets_frontend': [
            'vixo_add_to_quotation_btn_1/static/src/scss/website.scss'
        ],
    },
    'demo': [
    ],
    'images': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
