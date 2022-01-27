# -*- coding: utf-8 -*-

{
	'name': """
		PLE Libro Registro de Ventas Reportes Sunat Perú TXT XLS |
        PLE Sale Register Book Sunat Peru TXT XLS Reports
    """,

    'summary': """
        Permite generar los libros de 14.1 y 14.2 PLE de Sunat Perú. |
        Allows to generate the 14.1 y 14.2 PLE of Sunat Peru.
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
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
		'dv_l10n_pe_sunat_ple_base',
	],
	'data': [
     	'security/ple_security.xml',
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