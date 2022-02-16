from odoo import models, fields


class stork(models.Model):
    # Heredamos campos del modelo vehicle
    _inherit = ['fleet.vehicle']

    # Personalizacion de los campos
    # _name = 'trip.storks'
    _description = 'Ciguenias Cervintes'
    # _rec_name = 'code'
    # Campos añadidos
    stork_code = fields.Char(string='Código de cigueña', required=True)
    # placa = fields.Char(string='Placa', required=True)
    # model = fields.Char(string='Modelo', required=True)
