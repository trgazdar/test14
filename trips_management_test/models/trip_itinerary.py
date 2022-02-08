from odoo import models, fields


class itinerary(models.Model):
    _name = 'trip.itinerary'
    _description = 'Itinerarios Servintes'
    _rec_name = 'description'
    # DATOS DEL ITINERARIO
    description = fields.Char(string='Descripcion', required=True)
    tax = fields.Float(string='Tarifa', required=True)

    # FOREING KEYS
    # trip_trip_id = fields.Many2one('trip.trip', string="Nro de Viaje")
    # trip_sourcing_ids = fields.One2many('trip.sourcing', 'trip_itinerary_id', string="Abastecimientos")
