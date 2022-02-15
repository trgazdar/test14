# -*- coding: utf-8 -*-
{
    'name': "trips_management_test",

    'summary': """
        Modulo que crea y gestiona viajes""",

    'description': """
        Modulo que crea y gestiona viajes
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/control_guias_views.xml',
        'views/menus_actions.xml',
        'views/trip_sourcing.xml',
        'views/trip_section.xml',
        'views/trip_trip.xml',
        'security/ir_model_access.xml',
    ],
}
