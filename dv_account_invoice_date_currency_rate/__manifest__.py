{
    'name': """
        Account Invoice Date Currency Rate. |
        Tipo de cambio a la fecha de emision de la Factura
    """,

    'summary': """
        Converts the invoice currency to the currency rate of the invoice date |
        Conversion a Tipo de cambio a la fecha de emision de la factura.
    """,

    'description': """
        Converts the invoice currency to the currency rate of the invoice date. |
        Conversion a Tipo de cambio a la fecha de emision de la factura.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'price': 39.99,
    'currency': 'EUR',

    'depends': [
        'account',
    ],

    'data': [
        'views/account_move_views.xml',
    ],

    'images': ['static/description/banner.gif'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
