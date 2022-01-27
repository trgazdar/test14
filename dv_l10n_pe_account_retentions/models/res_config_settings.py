from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    withholding_account_id = fields.Many2one('account.account', string="Cuenta de retención",
                                             domain=lambda self: [
                                                 ('deprecated', '=', False)],
                                             help="Cuenta que será utilizada para registrar la deuda de retenciones.")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    withholding_account_id = fields.Many2one(
        'account.account', string='Cuenta de retención',
        related='company_id.withholding_account_id', readonly=False,
        domain=lambda self: [('deprecated', '=', False)],
        help="Cuenta que será utilizada para registrar la deuda de retenciones.")
