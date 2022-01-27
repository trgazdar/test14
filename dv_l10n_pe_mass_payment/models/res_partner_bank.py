from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    # TODO agregarlo en todas las vistas
    account_type = fields.Selection([
        ('saving_account', 'Cuenta de Ahorros'),
        ('current_account', 'Cuenta Corriente'),
        ('master_account', 'Cuenta Maestra'),
        ('interbank_account', 'Cuenta Interbancaria'),
    ], string='Tipo de cuenta', required=True)

    account_type_code = fields.Char(
        string='Codigo del tipo de cuenta', compute='_compute_account_type_code')
    is_bank_bcp = fields.Char(string='Es cuenta BCP',
                              compute='_compute_is_bank_bcp')
    currency_short_code = fields.Char(string='Tipo moneda de abono',related='currency_id.short_code')

    def _compute_is_bank_bcp(self):
        for record in self:
            if record.bank_id.name == 'BCP':
                code = 'S'
            else:
                code = 'N'
            record.is_bank_bcp = code

    def _compute_account_type_code(self):
        for record in self:
            acc_type = record.account_type
            if acc_type == 'saving_account':
                account_type_code = 'A'
            elif acc_type == 'current_account':
                account_type_code = 'C'
            elif acc_type == 'master_account':
                account_type_code = 'M'
            elif acc_type == 'interbank_account':
                account_type_code = 'B'
            else:
                account_type_code = False
            record.account_type_code = account_type_code

    # Validación de cantidad de digitos segun el banco y el tipo de cuenta
    @api.constrains('acc_number','account_type')
    def _check_acc_number(self):
        for record in self:
            if record.account_type == 'saving_account' and record.bank_id.saving_account_digits and len(record.acc_number) != record.bank_id.saving_account_digits:
                raise ValidationError(
                    'La cantidad de digitos no coincide con una cuenta de ahorros para este banco.')
            elif record.account_type == 'current_account' and record.bank_id.current_account_digits and len(record.acc_number) != record.bank_id.current_account_digits:
                raise ValidationError(
                    'La cantidad de digitos no coincide con una cuenta corriente para este banco.')
            elif record.account_type == 'current_account' and record.bank_id.cci_account_digits and len(record.acc_number) != record.bank_id.cci_account_digits:
                raise ValidationError(
                    'La cantidad de digitos no coincide con una cuenta interbancaria para este banco.')
            else:
                return True
