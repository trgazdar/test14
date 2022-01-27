from odoo import api, fields, models


class Curreny(models.Model):
    _inherit = 'res.currency'

    short_code = fields.Char(string='Codigo corto')