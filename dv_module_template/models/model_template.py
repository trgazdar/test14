from odoo import api, fields, models


class ModelTemplate(models.Model):
    _name = 'model.template'
    _description = 'Modelo Plantilla'

    full_name = fields.Char(string='Apellidos y nombres')
    
