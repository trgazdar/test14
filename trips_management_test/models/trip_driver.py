from odoo import models, fields


class driver(models.Model):
    _name = 'trip.driver'
    _description = 'Operadores(conductores) de la empresa'

    # DATOS DEL OPERADOR
    name = fields.Char(string='Nombres', required=True)
    surname = fields.Char(string='Apellidos', required=True)
    dni = fields.Char(string='DNI', required=True)

    # FOREING KEYS
    # trip_trip_id = fields.Many2one('trip.trip', string="Nro de Viaje")
    # trip_sourcing_ids = fields.One2many('trip.sourcing', 'trip_driver_id', string="Abastecimientos")
