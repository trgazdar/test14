import base64
import requests
from odoo import api, fields, models

class BodyOrgan(models.Model):
    _name = 'body.organ'
    _inherit = ['image.mixin']
    _description = 'Organos del cuerpo'

    name = fields.Char(string='Nombre del órgano', required=True)
    description = fields.Text(string='Descripción')
    internal_code = fields.Char(string='Código interno')  

    function_ids = fields.One2many(
        'body.function', 'organ_id', string='Función')

    system_ids = fields.One2many(
        'body.system', compute='_compute_systems', readonly=False)

    def _compute_systems(self):
        for record in self:
            system_list = []
            for function in record.function_ids:
                system_list.append(function.system_id.id)
            record.system_ids = [(6, 0, list(set(system_list)))]

    illness_ids = fields.One2many(
        'body.illness', compute='_compute_illnesses', readonly=False, string='Síntomas')

    def _compute_illnesses(self):
        for record in self:
            illness_list = []
            for function in record.function_ids:
                illness_list += function.illness_ids.ids
            record.illness_ids = [(6, 0, list(set(illness_list)))]

    disease_ids = fields.One2many(
        'body.disease', compute='_compute_diseases', readonly=False, string='Enfermedades que lo afectan')

    def _compute_diseases(self):
        for record in self:
            disease_list = []
            for function in record.function_ids:
                disease_list += function.disease_ids.ids
            record.disease_ids = [(6, 0, list(set(disease_list)))]

    logo = fields.Image(
        "Icono de la sede", max_width=128, max_height=128, store=True)

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
