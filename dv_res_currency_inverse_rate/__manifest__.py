{
    'name': """
        Currency Inverse Rate
        Tipo de Cambio inverso al de Odoo
    """,   

    'summary': """
        Allows to write a currency rate in an inverse format
        Agrega el tipo de cambio inverso para paises que utilizan un formato diferente al de Odoo.
    """,

    'description': """
        Agrega el tipo de cambio inverso para paises que utilizan un formato diferente al de Odoo.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Sale',
    'version': '14.0',

    'price': 19.99,
    'currency': 'EUR',

    'depends': [
        'base',
        'sale_management', 
    ],

    'data': [
        'views/res_currency_views.xml',
        'views/res_currency_rate_views.xml',
    ],
        
    'images': ['static/description/banner.png'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
