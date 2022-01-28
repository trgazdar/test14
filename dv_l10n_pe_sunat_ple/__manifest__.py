{
    'name': """
        Reportes PLE Sunat Perú TXT XLS |
        PLE Sunat Peru TXT XLS Reports
    """,

    'summary': """
        Permite generar los libros de compras 8.1 8.2 8.3 y ventas 14.1 y 14.2 para el PLE de Sunat Perú. |
        Allows to generate the 8.1 8.2 8.3 and 14.1 and 14.2 books for the PLE of Sunat Peru.
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
        Permite generar reportes de los comprobantes de Compras y Ventas electrónicos a SUNAT en formato TXT y XLS.
        Registro de Facturas Electrónicas generadas en un periodo de tiepo.
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
        'l10n_pe',
        #'dv_l10n_pe_account_detractions',
        #'dv_account_move_withholding_tax',
        'dv_account_invoice_date_currency_rate',
        'dv_account_seat_number',
        'dv_l10n_pe_account_account',
    ],

    'data': [
        'views/account_move_views.xml',
        'views/ple_report_sale_views.xml',
        'views/ple_report_purchase_views.xml',
        'views/menu_item_views.xml',
        'security/ple_security.xml',
        'security/ir.model.access.csv',
    ],
    
    'images': ['static/description/banner.gif'],

    'application': True,
    'installable': True,
    'auto_install': False,
}
