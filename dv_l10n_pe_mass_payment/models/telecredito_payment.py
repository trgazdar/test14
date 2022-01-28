import base64
import xlwt
import platform

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class BCPMassPayment(models.Model):
    _name = 'telecredito.payment'
    _description = 'Pago masivo por Telecrédito'

    name = fields.Char(string='Descripción')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Compañía', required=True)
    start_date = fields.Date(string='Fecha Inicio', required=True)
    finish_date = fields.Date(string='Fecha Fin', required=True)
    invoice_high_priority = fields.Boolean(
        string='Prioridad Alta', default=True)
    invoice_medium_priority = fields.Boolean(string='Prioridad Media')
    invoice_low_priority = fields.Boolean(string='Prioridad Baja')

    invoice_payment_ids = fields.Many2many(
        'account.move', string='Factura a pagar')

    telecredito_xls_filename = fields.Char(
        string='Nombre del archivo Excel')
    telecredito_xls_file = fields.Binary(string='Reporte Excel')
    telecredito_txt_filename = fields.Char(
        string='Nombre del archivo TXT')
    telecredito_txt_file = fields.Binary(
        string='Reporte TXT')

    payment_state = fields.Selection(string='Estado de pago', selection=[
        ('not_paid', 'Sin pagar'),
        ('in_payment', 'Pagado,por conciliar'),
        ('paid', 'Cancelado')], compute='_compute_payment_state')
    
    def _compute_payment_state(self):
        for record in self:
            invoice_payment_states = record.invoice_payment_ids.mapped(
                'payment_state')
            if invoice_payment_states and 'not_paid' in invoice_payment_states:
                payment_state = 'not_paid'
            elif invoice_payment_states and 'in_payment' in invoice_payment_states:
                payment_state = 'in_payment'
            elif invoice_payment_states and 'partial' not in invoice_payment_states and 'reversed' not in invoice_payment_states and 'invoicing_legacy' not in invoice_payment_states:
                payment_state = 'paid'
            else:
                # Otro caso
                payment_state = 'not_paid'
            record.payment_state = payment_state

    # Función que trae las facturas de ventas del periodo indicado

    def get_invoice_payment_ids(self):
        # TODO consultar cuales son los que se reportan : Pagados, de que fecha a que fecha, si es la de creación o de vencimiento
        # TODO como es en el caso de devoluciones, se consideran? hay un registro a parte?
        priorities = []
        if self.invoice_high_priority:
            priorities.append('high')
        if self.invoice_medium_priority:
            priorities.append('medium')
        if self.invoice_low_priority:
            priorities.append('low')

        invoice_to_pay_ids = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('company_id', '=', self.company_id.id),
            # TODO agregar notas de debito o credito correspondientes a las facturas que se van a pagar
            ('payment_priority', 'in', priorities),
            ('move_type', '=', 'in_invoice'),
            ('payment_state', '=', 'not_paid'),
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.finish_date)
        ], order='id asc')
        # IDEA DE NOTAS DE CREDITO
        invoice_reversed_ids = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('company_id', '=', self.company_id.id),
            ('reversed_entry_id', 'in', invoice_to_pay_ids.ids),
            ('move_type', '=', 'in_refund'),
        ], order='id asc')
        self.write({
            'telecredito_xls_filename': False,
            'telecredito_xls_file': False,
            'telecredito_txt_filename': False,
            'telecredito_txt_file': False,
            'invoice_payment_ids': invoice_to_pay_ids + invoice_reversed_ids,
        })

    def validate_date_filters(self):
        for record in self:
            if record.end_date and record.end_date < record.start_date:
                record.end_date = False
                raise ValidationError(
                    'La fecha fin debe ser mayor a la fecha de inicio.')

    def _generate_telecredito_txt_filename(self):
        return f"{self.name}.txt"

    def _generate_telecredito_xls_filename(self):
        return f"{self.name}.xls"

    def _write_excel_header(self, sheet):
        sheet.write(0, 0, 'Tipo de Registro')
        sheet.write(0, 1, 'Tipo de Cuenta de Abono')
        sheet.write(0, 2, 'Cuenta de Abono')
        sheet.write(0, 3, 'Tipo de Documento de Identidad')
        sheet.write(0, 4, 'Número de Documento de Identidad')
        sheet.write(0, 5, 'Correlativo de Documento de Identidad')
        sheet.write(0, 6, 'Nombre del proveedor')
        sheet.write(0, 7, 'Tipo de Moneda de Abono')
        sheet.write(0, 8, 'Monto del Abono')
        sheet.write(0, 9, 'Validación IDC del proveedor vs Cuenta')
        sheet.write(0, 10, 'Cantidad Documentos relacionados al Abono')
        sheet.write(0, 11, 'Tipo de Documento a pagar')
        sheet.write(0, 12, 'Nro. del Documento')
        sheet.write(0, 13, 'Moneda Documento')
        sheet.write(0, 14, 'Monto del Documento')
        sheet.write(0, 15, '')
        sheet.write(0, 16, 'CORREO')
        return sheet

    def _write_partner_data(self, sheet, partner_row, partner, total_amount, invoice_quantity):
        sheet.write(partner_row, 0, 'A')
        sheet.write(partner_row, 1,
                    partner.default_bank_account.account_type_code)
        sheet.write(partner_row, 2, partner.default_bank_account.acc_number)
        sheet.write(partner_row, 3,
                    partner.l10n_latam_identification_type_id.l10n_pe_vat_code)
        sheet.write(partner_row, 4, partner.vat)
        sheet.write(partner_row, 5, '')
        sheet.write(partner_row, 6, partner.name)
        # Validar que siempre se pagara en soles
        sheet.write(partner_row, 7, 'S')
        sheet.write(partner_row, 8, total_amount)
        sheet.write(partner_row, 9, partner.default_bank_account.is_bank_bcp)
        sheet.write(partner_row, 10, invoice_quantity)
        return sheet

    def generate_telecredito_xls_file(self):
        for record in self:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('Facturas a pagar')
            sheet = self._write_excel_header(sheet)

            row = 1
            invoice_to_pay_by_partner_ids = record.invoice_payment_ids.sorted(
                lambda m: m.partner_id)
            current_partner = ''
            for acc_mov in invoice_to_pay_by_partner_ids:
                if acc_mov.partner_id != current_partner:
                    current_partner = acc_mov.partner_id
                    partner_invoices = invoice_to_pay_by_partner_ids.filtered(
                        lambda x: x.partner_id.id == current_partner.id)
                    partner_invoice_total_amount = 0
                    invoice_quantity = 0
                    for inv in partner_invoices:
                        partner_invoice_total_amount += inv.amount_total
                        invoice_quantity += 1
                    invoice_quantity = str(invoice_quantity).zfill(4)
                    # primera fila , datos de proveedor
                    sheet.write(row, 0, 'A')
                    sheet.write(
                        row, 1, current_partner.default_bank_account.account_type_code)
                    sheet.write(
                        row, 2, current_partner.default_bank_account.acc_number)
                    sheet.write(
                        row, 3, current_partner.l10n_latam_identification_type_id.l10n_pe_vat_code)
                    sheet.write(row, 4, current_partner.vat)
                    sheet.write(row, 5, '')
                    sheet.write(row, 6, current_partner.name)
                    # Validar que siempre se pagara en soles
                    sheet.write(row, 7, 'S')
                    sheet.write(row, 8, partner_invoice_total_amount)
                    sheet.write(
                        row, 9, current_partner.default_bank_account.is_bank_bcp)
                    sheet.write(row, 10, invoice_quantity)
                    row += 1

                sheet.write(row, 0, 'D')
                sheet.write(row, 11, acc_mov.get_document_type_letter())
                sheet.write(
                    row, 12, acc_mov.get_invoice_telecredito_payment_name())
                sheet.write(row, 13, acc_mov.get_currency_letter())
                sheet.write(row, 14, acc_mov.amount_total)
                row += 1

            if platform.system() == 'Linux':
                filename = ('/tmp/telecredito_payment' + '.xls')
            else:
                filename = ('telecredito_payment' + '.xls')
            workbook.save(filename)
            fp = open(filename, "rb")
            file_data = fp.read()

            record.write({
                'telecredito_xls_filename': record._generate_telecredito_xls_filename(),
                'telecredito_xls_file': base64.b64encode(file_data)
            })

    def action_register_payment(self):
        return {
            'name': 'Registrar Pago',
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.invoice_payment_ids.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
