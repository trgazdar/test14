from odoo import api, fields, models


class Disease(models.Model):
    _name = 'body.disease'
    _description = 'Enfermedades del cuerpo'

    name = fields.Char(string='Nombre de la enfermedad', required=True)
    internal_code = fields.Char(string='Código interno')

    description = fields.Text(string='Descripción')

    illness_ids = fields.One2many(
        'body.illness', 'disease_id', string='Síntomas')

    function_ids = fields.One2many(
        'body.function', compute='_compute_functions', string='Funciones', readonly=False)

    def _compute_functions(self):
        for record in self:
            function_list = []
            for illness in record.illness_ids:
                function_list.append(illness.function_id.id)
            record.function_ids = [(6, 0, list(set(function_list)))]

    organ_ids = fields.One2many(
        'body.organ', compute='_compute_organs', readonly=False, string='Organos')

    def _compute_organs(self):
        for record in self:
            organ_list = []
            for function in record.function_ids:
                organ_list.append(function.organ_id.id)
            record.organ_ids = [(6, 0, list(set(organ_list)))]

    system_ids = fields.One2many(
        'body.system', compute='_compute_systems', readonly=False, string='Sistemas')

    def _compute_systems(self):
        for record in self:
            system_list = []
            for organ in record.organ_ids:
                system_list += organ.system_ids.ids
            record.system_ids = [(6, 0, list(set(system_list)))]
