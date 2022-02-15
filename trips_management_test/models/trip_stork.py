from odoo import models, fields


class stork(models.Model):
    _name = 'trip.stork'
    _description = 'Ciguenias Cervintes'
    _rec_name = 'code'
    # DATOS DEL OPERADOR
    code = fields.Char(string='Código', required=True)
    placa = fields.Char(string='Placa', required=True)
    model = fields.Char(string='Modelo', required=True)
