{
    'name': """
        Menu de creación de Tipo de Cambio
    """,

    'summary': """
        Agrega un menu para la creación rápida de tipos de cambio.
    """,

    'description': """
        Agrega un menu para la creación rápida de tipos de cambio.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Invoice',
    'version': '14.0',
    
    'price': 19.99,
    'currency': 'EUR',

    'depends': [
        'account',
    ],

    'data': [
        'wizard/res_currency_rate_wizard_views.xml',
        'views/menu_item_views.xml',
        'security/ir.model.access.csv',
    ],
    
    'images': ['static/description/banner.png'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
