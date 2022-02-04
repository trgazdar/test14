from odoo import models, fields


class trip(models.Model):
    _name = 'trip.trip'
    _description = 'Viajes'

    nro_viaje = fields.Char(string='Nro. Viaje', required=True)
    nro_rendicion = fields.Char(string='Nro. Rendicion', required=True)
    delivery_date = fields.Date(string='Fecha de Entrega', required=True)
    paica_cod_tracto = fields.Char(string='PAIca /Cod. Tracto', required=True)
    shipment = fields.Char(string='Carga', required=True)
    no_axles = fields.Integer(string='Nro. Ejes', required=True)
    no_invoice = fields.Integer(string='Nro. Facturas', required=True)
    given_amount = fields.Char(string='Monto entregado', required=True)

    # Foreing keys
    itinerary_id = fields.Char(string='Itinerario', required=True)
    stork_id = fields.Char(string='Cigûeña', required=True)
    driver_id = fields.Char(string='Operador', required=True)
    trip_section_ids = fields.One2many('trip.section', 'trip_trip_id', string='Tramos de un viaje', required=True)
