# -*- coding: utf-8 -*-

{
	'name': """
        PLE Libro Mayor Reportes Sunat Perú TXT XLS |
        PLE Major Book Sunat Peru TXT XLS Reports
    """,

    'summary': """
        Permite generar los libros de 6.1 PLE de Sunat Perú. |
        Allows to generate the 6.1 PLE of Sunat Peru.
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE
        SUNAT PLE
        PLE SUNAT
        Libro Mayor
        Libro 6.1
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'price': 119.99,
    'currency': 'EUR',
	
	'depends': [
     	'base',
		'dv_l10n_pe_sunat_ple',
	],
	'data': [
     	'security/ple_report_security.xml',
		'security/ir.model.access.csv',
		'views/ple_report_views.xml',
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
