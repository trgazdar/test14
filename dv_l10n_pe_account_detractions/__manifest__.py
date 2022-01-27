{
    'name': """
        Facturas con Detracciones Perú. |
        Invoice with Detraction Taxes Report Peru. |
    """,

    'summary': """
        Permite generar facturas con impuestos de detracción. |
        Allows to generate invoices with detraction taxes.
    """,

    'description': """
        Agrega campos de impuestos de detracción en facturas de proveedor y genera el asiento contable al confirmar la factura. |
        Adds detraction taxes fields in supplier invoices and generates the accounting entry when confirming the invoice.
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Accounting',
    'version': '14.0',
    
    'price': 49.99,
    'currency': 'EUR',

    'depends': [
        'base',
        'account',
    ],

    'data': [
        'data/l10n_pe_detraction.table.csv',
        'views/account_move_views.xml',
        'views/res_config_settings_views.xml',
        'views/drawdown_tax_table_views.xml',
        'views/menu_item_views.xml',
        'security/ir.model.access.csv',
    ],
    
    'images': ['static/description/banner.png'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
