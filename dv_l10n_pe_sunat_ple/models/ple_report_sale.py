from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class PLESale(models.Model):
    _inherit = 'ple.report'
    _name = 'ple.report.sale'
    _description = 'Reporte de Ventas PLE'

    period_invoice_ids = fields.One2many(
        comodel_name='account.move', string='Factura de ventas', compute='_compute_period_invoice_ids')

    ple_14_1_txt_filename = fields.Char(
        string='Nombre archivo TXT 14.1')
    ple_14_1_txt_file = fields.Binary(
        string='Reporte TXT 14.1')
    ple_14_1_xls_filename = fields.Char(
        string='Nombre archivo Excel 14.1')
    ple_14_1_xls_file = fields.Binary(string='Reporte Excel 14.1')

    ple_14_2_txt_filename = fields.Char(
        string='Nombre archivo TXT 14.2')
    ple_14_2_txt_file = fields.Binary(
        string='Reporte TXT 14.2')
    ple_14_2_xls_filename = fields.Char(
        string='Nombre archivo Excel 14.2')
    ple_14_2_xls_file = fields.Binary(string='Reporte Excel 14.2')

    def _compute_period_invoice_ids(self):
        for record in self:
            record.period_invoice_ids = self.env['account.move'].search([
                ('state', 'in', ['posted','cancel']),
                ('company_id', '=', record.company_id.id),
                ('move_type', 'in', ['out_invoice',
                                     'out_refund', 'out_receipt']),
                ('date', '>=', record.start_date),
                ('date', '<=', record.finish_date)
            ], order='create_date asc')
            
    def generate_ple_txt_files(self):
        self.generate_ple_txt_file('14_1')
        self.generate_ple_txt_file('14_2')
        self.write({'report_state': 'created','txt_creation_datetime': fields.Datetime.now()})
        
    def generate_ple_xls_files(self):
        self.generate_ple_xls_file('14_1')
        self.generate_ple_xls_file('14_2')
        self.write({'xls_creation_datetime': fields.Datetime.now()})
        
