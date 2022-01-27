from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move' 
    payment_priority = fields.Selection([('high', 'Alta'),
                                         ('medium', 'Media'),
                                         ('low', 'Baja')], string='Prioridad de pago')
    payment_planned_date = fields.Date(string='Fecha de pago planeada')
    
    l10n_pe_partner_vat = fields.Char(
        'Número de identificación', related='partner_id.vat')
    
    l10n_pe_invoice_serial = fields.Char(
        string='Serie', compute='_compute_invoice_serial_number')
    l10n_pe_invoice_number = fields.Char(
        string='Numero correlativo', compute='_compute_invoice_serial_number')
    def _compute_invoice_serial_number(self):
        for record in self:
            invoice_serial = False
            invoice_number = False
            if record.l10n_latam_use_documents and record.l10n_latam_document_number:
                seq_split = record.l10n_latam_document_number.split('-')
                if len(seq_split) == 2:
                    invoice_serial = seq_split[0]
                    invoice_number = seq_split[1]
            else:
                seq_split = record.name.split('-')
                if len(seq_split) == 2:
                    invoice_serial = seq_split[0]
                    invoice_number = seq_split[1]
            
            record.write({
                'l10n_pe_invoice_serial': invoice_serial,
                'l10n_pe_invoice_number': invoice_number,
            })
    
    def get_document_type_letter(self):
        if self.l10n_latam_document_type_id.code == '01':
            document_letter = 'F'
        elif self.l10n_latam_document_type_id.code == '03':
            document_letter = 'B'
        else:
            document_letter = False
        return document_letter

    def get_currency_letter(self):
        if self.currency_id.name == 'PEN':
            currency_letter = 'S'
        elif self.currency_id.name == 'USD':
            currency_letter = 'D'
        else:
            currency_letter = False
        return currency_letter
    
    def get_invoice_telecredito_payment_name(self):
        # Por defecto al almacén que primero llega la mercaderia
        # self.l10n_pe_edi_warehouse_id.payment_internal_code
        # TODO todo en mayus
        return f"A {self.l10n_pe_invoice_serial} {self.l10n_pe_invoice_number}"
    
    def open_record(self):
        # first you need to get the id of your record
        # you didn't specify what you want to edit exactly
        rec_id = self.id
        # then if you have more than one form view then specify the form id
        form_id = self.env.ref('account.view_move_form')

        # then open the form
        return {
            'type': 'ir.actions.act_window',
            'name': 'title',
            'res_model': 'account.move',
            'res_id': rec_id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            # if you want to open the form in edit mode direclty
            'flags': {'initial_mode': 'edit'},
            'target': 'current',
        }
