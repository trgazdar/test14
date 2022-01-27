from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    default_bank_account = fields.Many2one('res.partner.bank',
        string='Cuenta bancaria por defecto', compute='_compute_default_bank_account')

    def _compute_default_bank_account(self):
        for record in self:
            default_bank_account = self.env['res.partner.bank'].search(
                [('partner_id', '=', record.id)], limit=1)
            record.default_bank_account = default_bank_account
