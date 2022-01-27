from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_pe_edi_is_sale_credit = fields.Boolean(string="Sale on Credit", compute='_get_is_sale_credit', store=True)
    
    @api.depends('invoice_payment_term_id', 'invoice_date', 'invoice_date_due')
    def _get_is_sale_credit(self):
        self.l10n_pe_edi_is_sale_credit = False
        for move in self:
            #if move.l10n_latam_document_type_id.code == '01' and move.move_type == 'out_invoice':
            # CPE
            if move.journal_id.pe_invoice_code == '01' and move.move_type == 'out_invoice':
                if move.invoice_payment_term_id:
                    if len(move.invoice_payment_term_id.line_ids) > 1:
                        move.l10n_pe_edi_is_sale_credit = True
                    else:
                        payment_term_line = move.invoice_payment_term_id.line_ids[0]
                        if payment_term_line.value == 'balance' and payment_term_line.days > 0:
                            move.l10n_pe_edi_is_sale_credit = True
                else:
                    if move.invoice_date_due and move.invoice_date_due > (move.invoice_date or fields.Date.today()):
                        move.l10n_pe_edi_is_sale_credit = True
                        
                        
    l10n_pe_edi_dues_ids = fields.One2many('l10n_pe_edi.dues', 'move_id', string='Dues')
    
    def _get_dues_ids(self):
        if self.l10n_pe_edi_is_sale_credit:
            self.l10n_pe_edi_dues_ids = False
            number = 0
            dues = []
            for line in self.line_ids.filtered(lambda x: x.exclude_from_invoice_tab and x.date_maturity != False and x.debit > 0.0):
                number += 1
                vals = {
                    'move_id': self.id,
                    'dues_number': number,
                    'paid_date': line.date_maturity,
                    'amount': abs(line.amount_currency),
                }
                dues.append((0,0,vals))
            self.l10n_pe_edi_dues_ids = dues
            
    @api.onchange('line_ids', 'invoice_payment_term_id', 'invoice_date_due', 'invoice_cash_rounding_id', 'invoice_vendor_bill_id')
    def _onchange_recompute_dynamic_lines(self):
        super(AccountMove, self)._onchange_recompute_dynamic_lines()
        self._get_dues_ids()