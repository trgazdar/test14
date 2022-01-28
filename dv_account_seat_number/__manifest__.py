{
    'name': """
        Seat Sequence number for journal entries and Invoices |
        Número de asiento o correlativo para facturas y asientos contables
    """,

    'summary': """
        Automaticaly assign a seat number to bills, invoices and journal entries. |
        Automáticamente asigna un número de asiento o correlativo a facturas, asientos contables y asientos de diario.
    """,

    'description': """
        Grouping of accounting entries by journals and generate a unique sequence for each journal group, every entry of the journal will follow the sequence and show it on the invoice form and tree view. |
        Agrupación de asientos contables por diarios y generación de una secuencia única para cada grupo de diarios, cada asiento del diario seguirá la secuencia y se mostrará en la vista formulario y árbol de factura y de asientos contables.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'price': 49.99,
    'currency': 'EUR',

    'depends': [
        'base',
        'account',
    ],

    'data': [
        'views/account_journal_group_views.xml',
        'views/account_move.xml',
    ],

    'images': ['static/description/banner.gif'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
