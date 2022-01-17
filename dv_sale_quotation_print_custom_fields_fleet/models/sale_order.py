from odoo import api, fields, models, _
from num2words import num2words

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # === Amount fields ===
    l10n_pe_edi_amount_subtotal = fields.Monetary(string='Subtotal',store=True, readonly=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True, help='Total without discounts and taxes')
    l10n_pe_edi_amount_discount = fields.Monetary(string='Total Discount', store=True, readonly=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)    
    l10n_pe_edi_amount_base = fields.Monetary(string='Base Amount', store=True, readonly=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True, help='Total with discounts and before taxes')
    l10n_pe_edi_amount_advance = fields.Monetary(string='Advance Amount', store=True, readonly=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)
    l10n_pe_edi_amount_exonerated = fields.Monetary(string='Exonerated  Amount', store=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)
    l10n_pe_edi_amount_free = fields.Monetary(string='Free Amount', store=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)
    l10n_pe_edi_amount_unaffected = fields.Monetary(string='Unaffected Amount', store=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)      
    l10n_pe_edi_amount_untaxed = fields.Monetary(string='Total before taxes', store=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True, help='Total before taxes, all discounts included')   
    l10n_pe_edi_global_discount = fields.Monetary(string='Global discount', store=True, readonly=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)  
    l10n_pe_edi_amount_in_words = fields.Char(string="Amount in Words", compute='_l10n_pe_edi_amount_in_words')
    l10n_pe_edi_amount_in_words = fields.Char(string="Monto en palabras", compute='_l10n_pe_edi_amount_in_words')
    
    l10n_pe_edi_amount_icbper = fields.Monetary(string='ICBPER Amount', compute='_compute_edi_amount', compute_sudo=True, tracking=True)
    l10n_pe_edi_amount_igv = fields.Monetary(string='IGV Amount', compute='_compute_edi_amount', compute_sudo=True, tracking=True)
    l10n_pe_edi_amount_isc = fields.Monetary(string='ISC Amount', store=True, compute='_compute_edi_amount', compute_sudo=True, tracking=True)
    l10n_pe_edi_amount_others = fields.Monetary(string='Other charges', compute='_compute_edi_amount', compute_sudo=True, tracking=True)  
    
    @api.depends('amount_total','currency_id')
    def _l10n_pe_edi_amount_in_words(self):
        """Transform the amount to text
        """
        for move in self:
            amount_base, amount = divmod(move.amount_total, 1)
            amount = round(amount, 2)
            amount = int(round(amount * 100, 2))

            lang_code = self.env.context.get('lang') or self.env.user.lang
            lang = self.env['res.lang'].search([('code', '=', lang_code)])
            words = num2words(amount_base, lang=lang.iso_code)
            result = _('%(words)s CON %(amount)02d/100 %(currency_label)s') % {
                'words': words,
                'amount': amount,
                'currency_label': move.currency_id.name == 'PEN' and 'SOLES' or move.currency_id.currency_unit_label,
            }
            move.l10n_pe_edi_amount_in_words = result.upper()
    
    def _compute_edi_amount(self):
        for move in self:
            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            l10n_pe_edi_global_discount = 0.0
            l10n_pe_edi_amount_discount = 0.0
            l10n_pe_edi_amount_subtotal = 0.0
            l10n_pe_edi_amount_advance = 0.0
            #~ E-invoice amounts
            l10n_pe_edi_amount_free = 0.0
            currencies = set()

            sign = 1

            for line in move.order_line:
                if line.currency_id:
                    currencies.add(line.currency_id)
                if True:#move.is_invoice(include_receipts=True):
                    # === Invoices ===
                    # If the amount is negative, is considerated as global discount
                    l10n_pe_edi_global_discount += not line.l10n_pe_edi_regularization_advance and line.l10n_pe_edi_price_base < 0 and abs(line.l10n_pe_edi_price_base) or 0.0
                    # If the product is not free, it calculates the amount discount 
                    l10n_pe_edi_amount_discount += line.l10n_pe_edi_free_product == False and (line.l10n_pe_edi_price_base * line.discount)/100 or 0.0
                    # If the price_base is > 0, sum to the total without taxes and discounts
                    l10n_pe_edi_amount_subtotal += line.l10n_pe_edi_price_base > 0 and line.l10n_pe_edi_price_base or 0.0
                    # Free product amount
                    l10n_pe_edi_amount_free += line.l10n_pe_edi_amount_free
                    # If regularization advance is true, is considerated as advance
                    l10n_pe_edi_amount_advance += line.l10n_pe_edi_regularization_advance and line.l10n_pe_edi_price_base or 0.0
                # Affected by IGV
                if any(tax.l10n_pe_edi_tax_code in ['1000'] for tax in line.tax_id):
                    # Untaxed amount.
                    #total_untaxed += line.balance
                    #total_untaxed_currency += line.amount_currency
                    total_untaxed += line.price_subtotal
            #move.l10n_pe_edi_amount_base = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.l10n_pe_edi_amount_base = sign * (total_untaxed if len(currencies) == 1 else total_untaxed)
            # move.l10n_pe_edi_amount_base = sum([x[2] for x in move.amount_by_group if x[0] not in ['INA','EXO','EXP']])
            # Sum of Amount base of the lines where it has any Tax with code '9997'  (Exonerated)
            move.l10n_pe_edi_amount_exonerated = sum([x.l10n_pe_edi_price_base for x in move.order_line if any(tax.l10n_pe_edi_tax_code in ['9997'] for tax in x.tax_id)])
            # Sum of Amount base of the lines where it has any Tax with code in ['9998','9995']  (Unaffected and exportation)
            move.l10n_pe_edi_amount_unaffected = sum([x.l10n_pe_edi_price_base for x in move.order_line if any(tax.l10n_pe_edi_tax_code in ['9998','9995'] for tax in x.tax_id)])
            move.l10n_pe_edi_amount_igv = sum([x[1] for x in move.amount_by_group if x[0] == 'IGV'])
            move.l10n_pe_edi_amount_isc = sum([x[1] for x in move.amount_by_group if x[0] == 'ISC'])
            move.l10n_pe_edi_amount_icbper = sum([x[1] for x in move.amount_by_group if x[0] == 'ICBPER'])
            move.l10n_pe_edi_amount_others = sum([x[1] for x in move.amount_by_group if x[0] == 'OTROS'])
            move.l10n_pe_edi_amount_untaxed = move.l10n_pe_edi_amount_base - move.l10n_pe_edi_amount_free
            # TODO Global discount
            move.l10n_pe_edi_amount_advance = l10n_pe_edi_amount_advance
            move.l10n_pe_edi_global_discount = l10n_pe_edi_global_discount
            move.l10n_pe_edi_amount_discount = l10n_pe_edi_global_discount + l10n_pe_edi_amount_discount
            move.l10n_pe_edi_amount_subtotal = l10n_pe_edi_amount_subtotal
            move.l10n_pe_edi_amount_free = l10n_pe_edi_amount_free