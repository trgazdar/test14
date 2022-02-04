# -*- coding: utf-8 -*-
# from odoo import http


# class TripsManagementTest(http.Controller):
#     @http.route('/trips_management_test/trips_management_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trips_management_test/trips_management_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trips_management_test.listing', {
#             'root': '/trips_management_test/trips_management_test',
#             'objects': http.request.env['trips_management_test.trips_management_test'].search([]),
#         })

#     @http.route('/trips_management_test/trips_management_test/objects/<model("trips_management_test.trips_management_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trips_management_test.object', {
#             'object': obj
#         })
