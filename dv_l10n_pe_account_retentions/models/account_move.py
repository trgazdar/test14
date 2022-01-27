import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_subject_to_withholding = fields.Boolean(
        string='Sujeto a Retención')

    withholding_tax_table_id = fields.Many2one(
        'withholding.tax.table', string='Codigo de retención')
    account_withholding_percent = fields.Float(
        string='Porcentaje de retención', related='withholding_tax_table_id.percent', readonly=False)
    account_withholding_amount = fields.Monetary(
        string='Monto de retención', compute='_compute_withholding_amount')

    has_withholding_line = fields.Boolean(
        string='Tiene apunte de retención', compute='_compute_has_withholding_line', store=True)

    @api.depends('line_ids')
    def _compute_has_withholding_line(self):
        for record in self:
            has_withholding_line = False
            for line in record.line_ids:
                if line.is_withholding_line:
                    has_withholding_line = True
            record.has_withholding_line = has_withholding_line

    @api.depends('withholding_tax_table_id', 'amount_total')
    def _compute_withholding_amount(self):
        for record in self:
            account_withholding_amount = False
            if record.account_withholding_percent:
                account_withholding_amount = record.amount_total * \
                    record.account_withholding_percent
            record.account_withholding_amount = account_withholding_amount

    def _post(self, soft=True):
        for move in self:
            if move.is_subject_to_withholding and not move.company_id.withholding_account_id:
                raise UserError(_(
                    'No hay una cuenta de retención definida para la compañía %s.'
                    'Por favor defina una en la configuración.') % (
                    move.company_id.name))
            if move.withholding_tax_table_id and not move.has_withholding_line:
                line_data = {
                    'name': _('Retención'),
                    'ref': move.name,
                    'partner_id': move.partner_id and move.partner_id.id or False,
                    'currency_id': move.currency_id and move.currency_id.id or False,
                    'is_withholding_line': True,
                }
                debit_data = dict(line_data)
                credit_data = dict(line_data)

                if move.move_type in ('in_invoice', 'in_refund', 'in_receipt'):
                    debit_account_id = move.partner_id.property_account_payable_id.id
                    credit_account_id = move.company_id.withholding_account_id.id

                if move.move_type in ('out_invoice', 'out_refund', 'out_receipt'):
                    debit_account_id = move.company_id.withholding_account_id.id
                    credit_account_id = move.partner_id.property_account_receivable_id.id

                debit_data.update(
                    account_id=debit_account_id,
                    debit=move.account_withholding_amount,
                    credit=False,
                )
                credit_data.update(
                    account_id=credit_account_id,
                    debit=False,
                    credit=move.account_withholding_amount,
                )
                move.line_ids = [(0, 0, debit_data), (0, 0, credit_data)]
        res = super(AccountMove, self)._post(soft=soft)
        return res
