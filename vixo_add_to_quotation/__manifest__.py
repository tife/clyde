{
    'name': 'Add to quotation',
    'category': 'Website/eCommerce',
    'summary': 'Clyde eshop customisation',
    'description': 'Update quotation template. Add to quotation function. Email quotation to customer upon checkout',
    'version': '15.0.1.0.2',
    'author': 'Vixo Digital',
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
            'vixo_add_to_quotation/static/src/scss/sale_report.scss',
        ],
        'web.assets_frontend': [
            'vixo_add_to_quotation/static/src/scss/website.scss'
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
