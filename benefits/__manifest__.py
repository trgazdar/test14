{
    'name': "Beneficios",

    'summary': """
        Gestionar datos de partes del cuerpo humano y a la salud.
    """,

    'description': """
        Agrega nuevos modelos para definir partes del cuerpo, sus funciones y enfermedades.
    """,

    'author': "Ailton Salguero Bazalar",
    'website': "https://www.linkedin.com/in/ailton-salguero",

    'category': 'Foods',
    'version': '1.0',

    'depends': [
        'base',
    ],

    'data': [
        'security/benefits_security.xml',
        'views/body_function_views.xml',
        'views/body_illness_views.xml',
        'views/body_organ_views.xml',
        'views/body_system_views.xml',
        'views/body_disease_views.xml',
        'views/body_illness_views.xml',
        'views/menu_item_views.xml',
        'security/ir.model.access.csv',
    ],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
