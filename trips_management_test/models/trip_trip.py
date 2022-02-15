from odoo import models, fields


class trip(models.Model):
    _name = 'trip.trip'
    _description = 'Viajes'
    # Renombramos el campo identificador
    _rec_name = 'no_trip'

    # DATOS DEL VIAJE
    no_trip = fields.Char(string='Nro. Viaje', required=True)
    nro_rendicion = fields.Char(string='Nro. Rendicion', required=True)
    delivery_date = fields.Date(string='Fecha de Entrega', required=True)
    paica_cod_tracto = fields.Char(string='PAIca /Cod. Tracto', required=True)
    shipment = fields.Char(string='Carga', required=True)
    no_axles = fields.Integer(string='Nro. Ejes', required=True)
    no_invoice = fields.Integer(string='Nro. Facturas', required=True)
    given_amount = fields.Char(string='Monto entregado', required=True)
    state = fields.Char(string='Estado', required=True)

    # GASTOS DEL VIAJE
    viaticos = fields.Float(string='Viaticos', required=True)
    peajes = fields.Float(string='Peajes', required=True)
    otros_viajes = fields.Float(string='Otros viajes', required=True)
    drivers_payment = fields.Float(string='Pago al chofer', required=True)

    # FOREING KEYS
    itinerary_id = fields.Many2one('trip.itinerary', string="Itinerario", required=True)
    stork_id = fields.Many2one('trip.stork', string='Cigûeña', required=True)
    #driver_id = fields.Many2one('trip.driver', string='Operador', required=True)
    driver_id = fields.Many2one('res.partner', string='Operador', required=True)
    trip_section_ids = fields.One2many('trip.section', 'trip_trip_id', string='Tramos del viaje', required=True)
    trip_trip_detail_ids = fields.Many2many('control_guias', string='Detalles del viaje')#, required=True)

    # CAMPOS CALCULADOS
    # viaticos = fields.Float(string='Viaticos', required=True)
