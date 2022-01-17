{
    'name': """
        Plantillas de pedidos personalizables
    """,

    'summary': """
        Editar contenido de plantillas por compañía.
    """,

    'description': """
        Editar contenido de plantillas por compañía como cuentas bancarias, direcciones, celulares.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Website',
    'version': '14.0',
    
    'price': 79.99,
    'currency': 'EUR',

    'depends': [
        'base',
        'web',
        'sale',
        'sale_management',
    ],

    'data': [
        'views/res_company_views.xml',
        'views/sale_order_views.xml',
        'templates/external_layout_standard.xml',
        'templates/report_saleorder_document.xml',
    ],
    
    'images': ['static/description/banner.gif'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
