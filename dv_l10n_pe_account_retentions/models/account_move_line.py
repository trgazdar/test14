from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_withholding_line = fields.Boolean(string='Es apunte de retención')
