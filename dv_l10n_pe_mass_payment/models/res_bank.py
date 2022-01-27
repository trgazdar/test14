from odoo import api, fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'
    # Modelo que valida los
    saving_account_digits = fields.Integer(string='Cantidad de dígitos de cuenta de ahorros')
    current_account_digits = fields.Integer(string='Cantidad de dígitos de cuenta corriente')
    cci_account_digits = fields.Integer(string='Cantidad de dígitos de CCI')