import base64
import xlwt
import platform

from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class PleReportPurchase(models.Model):
    _inherit = 'ple.report'
    _name = 'ple.report.purchase'
    _description = 'Reporte de Compras PLE'

    period_invoice_ids = fields.One2many(
        comodel_name='account.move', string='Factura de compras', compute='_compute_period_invoice_ids')
    period_invoice_non_domic_ids = fields.One2many(
        comodel_name='account.move', string='Factura de compras no domiciliadas', compute='_compute_period_invoice_non_domic_ids')

    ple_8_1_txt_filename = fields.Char(
        string='Nombre archivo TXT 8.1')
    ple_8_1_txt_file = fields.Binary(
        string='Reporte TXT 8.1')
    ple_8_1_xls_filename = fields.Char(
        string='Nombre archivo Excel 8.1')
    ple_8_1_xls_file = fields.Binary(string='Reporte Excel 8.1')

    ple_8_2_txt_filename = fields.Char(
        string='Nombre archivo TXT 8.2')
    ple_8_2_txt_file = fields.Binary(
        string='Reporte TXT 8.2')
    ple_8_2_xls_filename = fields.Char(
        string='Nombre archivo Excel 8.2')
    ple_8_2_xls_file = fields.Binary(string='Reporte Excel 8.2')

    ple_8_3_txt_filename = fields.Char(
        string='Nombre archivo TXT 8.3')
    ple_8_3_txt_file = fields.Binary(
        string='Reporte TXT 8.3')
    ple_8_3_xls_filename = fields.Char(
        string='Nombre archivo Excel 8.3')
    ple_8_3_xls_file = fields.Binary(string='Reporte Excel 8.3')
     
    def _get_periord_format_report_invoice_ids(self,report_format='8_1'):
        if report_format == '8_2':
            period_invoice_ids = self.period_invoice_non_domic_ids
        else:
            period_invoice_ids = self.period_invoice_ids
        return period_invoice_ids
    
    def _compute_period_invoice_ids(self):
        for record in self:
            record.period_invoice_ids = self.env['account.move'].search([
                ('state', '=', 'posted'),
                ('l10n_latam_document_type_id.code','not in',['02','91','97','98']),
                ('l10n_pe_is_non_domiciled', '=', False),
                ('company_id', '=', record.company_id.id),
                ('move_type', 'in', ['in_invoice', 'in_refund', 'in_receipt']),
                ('date', '>=', record.start_date),
                ('date', '<=', record.finish_date)
            ], order='id asc')

    def _compute_period_invoice_non_domic_ids(self):
        for record in self:
            record.period_invoice_non_domic_ids = self.env['account.move'].search([
                ('state', '=', 'posted'),
                ('l10n_pe_is_non_domiciled', '=', True),
                ('company_id', '=', record.company_id.id),
                ('move_type', 'in', ['in_invoice', 'in_refund', 'in_receipt']),
                ('date', '>=', record.start_date),
                ('date', '<=', record.finish_date)
            ], order='id asc')
            
    def generate_ple_txt_files(self):
        self.generate_ple_txt_file('8_1')
        self.generate_ple_txt_file('8_2')
        self.generate_ple_txt_file('8_3')
        self.write({'report_state': 'created',
                    'txt_creation_datetime': fields.Datetime.now()})

    def generate_ple_xls_files(self):
        self.generate_ple_xls_file('8_1')
        self.generate_ple_xls_file('8_2')
        self.generate_ple_xls_file('8_3')
        self.write({'xls_creation_datetime': fields.Datetime.now()})
