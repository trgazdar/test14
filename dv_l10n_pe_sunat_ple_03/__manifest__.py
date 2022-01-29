# -*- coding: utf-8 -*-

{
    'name': """
        PLE Libro Inventarios y Balances Reportes Sunat Perú TXT XLS |
        PLE Inventories and Balances Sunat Peru TXT XLS Reports
    """,

    'summary': """
        Permite generar los libros de 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.11, 3.12, 3.13 y 3.14 PLE de Sunat Perú. |
        Allows to generate the 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.11, 3.12, 3.13 y 3.14 PLE of Sunat Peru.
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE
        SUNAT PLE
        PLE SUNAT
        Libro Inventarios y Balances
        Libro Inventarios
        Libro Balances
        Libro 3.1
        Libro 3.2
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'price': 199.99,
    'currency': 'EUR',

    'depends': [
            'base',
            'dv_l10n_pe_sunat_ple',
    ],
    'data': [
        'security/ple_report_security.xml',
        'security/ir.model.access.csv',
        'views/ple_report_views.xml',
        'views/product_template_views.xml',
    ],
    
    'images': ['static/description/banner.gif'],
    
    'external_dependencies': {
        'python': [
            'pandas',
            'xlsxwriter',
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': True,
}
