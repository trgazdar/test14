{
    'name': """
        MODULE NAME |
    """,

    'summary': """
        SUMMARY. |
    """,

    'description': """
        DESCRIPTION. |
    """,

    'author': 'Develogers',
    'website': 'https://develogers.com',
    'support': 'especialistas@develogers.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Invoice',
    'version': '1.0',

    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/model_template_views.xml',
    ],
    
    'images': ['static/description/banner.gif'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
