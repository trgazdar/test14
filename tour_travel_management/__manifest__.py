#  See LICENSE file for full copyright and licensing details.
{
    'name': 'Tours & Travels Management',
    'version': '14.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'sequence': 1,
    'license': 'AGPL-3',
    'category': 'Tours & Travels',
    'website': 'http://www.serpentcs.com',
    'depends': [
        'sale_margin',
        'purchase',
        'account_tax_python'
    ],
    'description': """
        Tours & Travels Management
    """,
    'summary': """
        Tours & Travels Management
    """,
    'data': [
        'security/travel_security.xml',
        'security/ir.model.access.csv',
        'data/package_product_data.xml',
        'data/package_contract_cron.xml',
        'data/package_sequence.xml',
        'views/supplier_registration_view.xml',
        'views/package_templates.xml',
        'views/travel_package_views.xml',
        'views/product_template_view.xml',
        'views/purchase_view.xml',
        'views/package_itinerary_views.xml',
        'views/product_category_views.xml',
        'views/city_city_views.xml',
#        'views/account_invoice_views.xml',
        'views/passenger_list_views.xml',
        'views/tour_registration_views.xml',
        'views/travelling_season_view.xml',
        'wizard/package_contract_cancel_wiz_view.xml',
        'views/package_contract_views.xml',
        'views/package_category_views.xml',
        'wizard/renew_contract_views.xml',
        'wizard/passenger_list_views.xml',
        'report/report_passenger_list.xml',
        'report/itinerary_report.xml',
        'report/report_quotation_tour_package.xml',
        'report/report_agreement.xml',
        'data/mail_data.xml',
        'views/manuitems.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [
        'demo/visa_status_demo.xml',
        'demo/travel_product_demo.xml',
        'demo/product_contract_demo.xml',
        'demo/tour_package_demo.xml',
    ],
    'uninstall_hook': 'test_uninstall_hook',
    'images': ['static/src/img/tour-pkg.jpg'],
    'installable': True,
    'application': True,
    'price': 57,
    'currency': 'EUR'
}
