from odoo import models, fields, api, _

class EdiDues(models.Model):
    _name = 'l10n_pe_edi.dues'
    _description = 'Dues'
    _order = 'dues_number'

    move_id = fields.Many2one('account.move', string="Move", required=True, readonly=True, ondelete="cascade")
    dues_number = fields.Integer(string="Dues Number")
    paid_date = fields.Date(string="Paid Date")
    amount = fields.Float(string="Amount")
