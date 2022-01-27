# -*- coding: utf-8 -*-

{
	'name': """
        Reportes PLE Libro Caja y Bancos Sunat Perú TXT XLS |
        PLE Sunat Peru TXT XLS Reports
    """,

    'summary': """
        Permite generar los libros de 1.1 y 1.2 PLE de Sunat Perú. |
        Allows to generate the 1.1 y 1.2 PLE of Sunat Peru.
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE
        SUNAT PLE
        PLE SUNAT
        Libro Caja y Bancos
        Libro Caja
        Libro Bancos
        Libro 1.1
        Libro 1.2
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
