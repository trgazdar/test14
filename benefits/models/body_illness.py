from odoo import api, fields, models


class BodyIllness(models.Model):
    _name = 'body.illness'
    _description = 'Síntomas del cuerpo'

    name = fields.Char(string='Nombre del síntoma', required=True)
    internal_code = fields.Char(string='Código interno')

    description = fields.Text(string='Descripción del síntoma')

    disease_id = fields.Many2one(
        'body.disease', string='Enfermedad que lo ocaciona', required=True)
    function_id = fields.Many2one(
        'body.function', string='Función a la que afecta', required=True)

    organ_id = fields.Many2one(
        'body.organ', related='function_id.organ_id', string='Síntoma')
    system_id = fields.Many2one(
        'body.system', related='function_id.system_id', string='Enfermedad')
    