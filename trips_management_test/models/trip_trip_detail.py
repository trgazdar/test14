from odoo import models, fields


class section(models.Model):
    _name = 'trip.trip.detail'
    _description = 'Detalle de un viaje'

    # Claves foraneas
    # trip_trip_id = fields.Many2one('trip.trip', string="Nro de Viaje")
    # guia_id = fields.Many2one('control_guias', 'trip_section_id', string="Abastecimientos")
