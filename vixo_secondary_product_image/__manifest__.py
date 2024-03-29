{
    'name': 'Secondary Product Image Hover',
    'summary': 'Secondary Product Image Hover',
    'description': 'When mouse of the product image, display the secondary proudct image. Add a product list component with "Borderless Product n*1" template. In the product carousel container, add a class "hover-sec-image" to enable this feature',
    'version': '1.0',
    'author': 'VIXO Digital Limited',
    'category': 'Website',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale'],
    'data': [
        'template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'vixo_secondary_product_image/static/src/scss/hover_sec_image.scss',
        ],
    },
}