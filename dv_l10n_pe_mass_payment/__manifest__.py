{
    'name': "Reporte XLS Pagos Masivos Telecredito BCP",

    'summary': """
        Generar reportes XLS Telecredito, registrar pago masivo de facturas, prioridad de pago de facturas.
    """,

    'description': """
        Generar reportes XLS Telecredito, registrar pago masivo de facturas, prioridad de pago de facturas.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'price': 199.99,
    'currency': 'EUR',

    'category': 'Accounting',
    'version': '14.0',

    'depends': [
        'base',
        'account',
        'l10n_pe',
        'stock',
    ],

    'data': [
        'views/account_move_views.xml',
        'views/res_bank_views.xml',
        'views/res_currency_views.xml',
        'views/res_partner_bank_views.xml',
        #'views/res_partner_views.xml',
        'views/stock_warehouse_views.xml',
        'views/telecredito_payment_views.xml',
        'views/menu_item_views.xml',
        'security/ir.model.access.csv',
        
        'wizard/setup_wizards_view.xml',
        'data/res.bank.csv',
    ],

    'images': ['static/description/banner.gif'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
