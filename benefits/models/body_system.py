import base64
import requests
from odoo import api, fields, models


class BodySystem(models.Model):
    _name = 'body.system'
    _inherit = ['image.mixin']
    _description = 'Sistema del cuerpo'

    name = fields.Char(string='Nombre del sistema', required=True)
    internal_code = fields.Char(string='Código interno')

    description = fields.Text(string='Descripción')

    function_ids = fields.One2many(
        'body.function', 'system_id', string='Funciones')

    organ_ids = fields.One2many(
        'body.organ', compute='_compute_organs', string='Organos', readonly=False)

    def _compute_organs(self):
        for record in self:
            organ_list = []
            for function in record.function_ids:
                organ_list.append(function.organ_id.id)
            record.organ_ids = [(6, 0, list(set(organ_list)))]

    illness_ids = fields.One2many(
        'body.illness', compute='_compute_illnesses', string='Síntomas')

    def _compute_illnesses(self):
        for record in self:
            illness_list = []
            for organ in record.organ_ids:
                illness_list += organ.illness_ids.ids
            record.illness_ids = [(6, 0, list(set(illness_list)))]

    disease_ids = fields.One2many(
        'body.disease', compute='_compute_diseases', readonly=False, string='Enfermedades')

    def _compute_diseases(self):
        for record in self:
            disease_list = []
            for organ in record.organ_ids:
                disease_list += organ.disease_ids.ids
            record.disease_ids = [(6, 0, list(set(disease_list)))]

    image_url = fields.Char(string='Imagen URL')
    odoo_image_url = fields.Char(
        string='URL a la imagen', compute='_compute_odoo_image_url')

    @api.depends('image_url')
    def _onchange_image_url(self):
        """ function to load image from URL """
        image = False
        if self.image_url:
            image = base64.b64encode(requests.get(self.image_url).content)
        self.image_1920 = image

    def _compute_odoo_image_url(self):
        web_base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        for record in self:
            record.odoo_image_url = f'{web_base_url}/web/image/{self._name}/{record.id}/image_256'
