from odoo import models, fields


class section(models.Model):
    _name = 'trip.section'
    _description = 'Secciones de un viaje'

    code = fields.Char(string='Codigo', required=True)
    departure_date = fields.Datetime(string='Fecha de salida', required=True)
    arrival_date = fields.Datetime(string='Fecha de llegada', required=True)

    # Claves foraneas
    trip_trip_id = fields.Many2one('trip.trip', string="Nro de Viaje")
    trip_sourcing_ids = fields.One2many('trip.sourcing','trip_section_id', string="Abastecimientos")
