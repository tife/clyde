{
    'name': 'Add to quotation',
    'category': 'Website/eCommerce',
    'summary': 'clyde custom.',
    'description': 'Update quotation template. Add to quotation function. Email quotation to customer upon checkout. Product Detail Page',
    'version': '15.0.1.0.2',
    'author': 'Vixo Digital',
    'data': [
        'views/product_template.xml',
        'views/product_template_views.xml',
        'views/attribute_value_views.xml',
        'views/cart_template.xml',
        'views/shop_template.xml',
        'report/sale_report.xml',
        'report/sale_report_template.xml',
        'views/header_template.xml',
        'views/footer_template.xml',
        'views/about_us_template.xml',
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
            'vixo_add_to_quotation/static/src/scss/website.scss',
            'vixo_add_to_quotation/static/src/scss/vixo_override.scss',
            'vixo_add_to_quotation/static/src/js/payment_status.js',
            'vixo_add_to_quotation/static/src/js/website_sale.js',
            'https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/assets/owl.carousel.min.css',
            'https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js',
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
