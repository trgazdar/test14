from odoo import api, fields, models


class BodyFunctions(models.Model):
    _name = 'body.function'
    _inherit = ['image.mixin']
    _description = 'Funciones del cuerpo'

    system_id = fields.Many2one(
        'body.system', string='Sistema del cuerpo', required=True)

    organ_id = fields.Many2one(
        'body.organ', string='Órgano', required=True)

    name = fields.Char(string='Nombre de la función', required=True)
    internal_code = fields.Char(string='Código interno')
    description = fields.Text(string='Descripción')

    illness_ids = fields.One2many(
        'body.illness', 'function_id', readonly=False, string='Síntomas')

    disease_ids = fields.One2many(
        'body.disease', compute='_compute_diseases', readonly=False, string='Enfermedades')

    def _compute_diseases(self):
        for record in self:
            disease_list = []
            for illness in record.illness_ids:
                disease_list.append(illness.disease_id.id)
            record.disease_ids = [(6, 0, list(set(disease_list)))]
