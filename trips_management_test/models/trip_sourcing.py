from odoo import models, fields


class sourcing(models.Model):
    _name = 'trip.sourcing'
    _description = 'Abastecimiento de un tramo '

    code = fields.Char(string='Codigo', required=True)
    station = fields.Char(string='Estación', required=True)
    odometer = fields.Char(string='Odómetro', required=True)

    # Claves foraneas
    trip_section_id = fields.Many2one('trip.section', string='Codigo de Tramo', required=True)

