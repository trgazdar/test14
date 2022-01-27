# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from .ple_report import get_last_day
from .ple_report import fill_name_data
from .ple_report import number_to_ascii_chr

import base64
import datetime
from io import StringIO, BytesIO
import pandas
import logging
_logging = logging.getLogger(__name__)


class PLEReport05(models.Model):
    _name = 'ple.report.05'
    _description = 'PLE 05 - Estructura del Libro Diario'
    _inherit = 'ple.report.templ'

    year = fields.Integer(required=True)
    month = fields.Selection(selection_add=[], required=True)

    line_ids = fields.Many2many(
        comodel_name='account.move.line', string='Movimientos', readonly=True)

    ple_txt_01 = fields.Text(string='Contenido del TXT 5.1')
    ple_txt_01_binary = fields.Binary(string='TXT 5.1', readonly=True)
    ple_txt_01_filename = fields.Char(string='Nombre del TXT 5.1')
    ple_xls_01_binary = fields.Binary(string='Excel 5.1', readonly=True)
    ple_xls_01_filename = fields.Char(string='Nombre del Excel 5.1')
    ple_txt_02 = fields.Text(string='Contenido del TXT 5.2')
    ple_txt_02_binary = fields.Binary(string='TXT 5.2', readonly=True)
    ple_txt_02_filename = fields.Char(string='Nombre del TXT 5.2')
    ple_xls_02_binary = fields.Binary(string='Excel 5.2', readonly=True)
    ple_xls_02_filename = fields.Char(string='Nombre del Excel 5.2')
    ple_txt_03 = fields.Text(string='Contenido del TXT 5.3')
    ple_txt_03_binary = fields.Binary(string='TXT 5.3', readonly=True)
    ple_txt_03_filename = fields.Char(string='Nombre del TXT 5.3')
    ple_xls_03_binary = fields.Binary(string='Excel 5.3', readonly=True)
    ple_xls_03_filename = fields.Char(string='Nombre del Excel 5.3')
    ple_txt_04 = fields.Text(string='Contenido del TXT 5.4')
    ple_txt_04_binary = fields.Binary(string='TXT 5.4', readonly=True)
    ple_txt_04_filename = fields.Char(string='Nombre del TXT 5.4')
    ple_xls_04_binary = fields.Binary(string='Excel 5.4', readonly=True)
    ple_xls_04_filename = fields.Char(string='Nombre del Excel 5.4')

    def get_default_filename(self, ple_id='050100', empty=False):
        name = super().get_default_filename()
        name_dict = {
            'month': str(self.month).rjust(2, '0'),
            'ple_id': ple_id,
        }
        if empty:
            name_dict.update({
                'contenido': '0',
            })
        fill_name_data(name_dict)
        name = name % name_dict
        return name

    def update_report(self):
        res = super().update_report()
        start = datetime.date(self.year, int(self.month), 1)
        end = get_last_day(start)
        #current_offset = fields.Datetime.context_timestamp(self, fields.Datetime.now()).utcoffset()
        #start = start - current_offset
        #end = end - current_offset
        lines = self.env.ref('base.pe').id
        lines = [
            ('company_id', '=', self.company_id.id),
            ('company_id.partner_id.country_id', '=', lines),
            ('move_id.state', '=', 'posted'),
            ('date', '>=', str(start)),
            ('date', '<=', str(end)),
        ]
        lines = self.env[self.line_ids._name].search(lines, order='date asc')
        self.line_ids = lines
        return res

    def generate_report(self):
        res = super().generate_report()
        lines_to_write_01 = []
        lines_to_write_02 = []
        lines_to_write_03 = []
        lines_to_write_04 = []
        lines = self.line_ids.sudo()
        move_dates = lines.mapped('date')
        for move_date in move_dates:
            date_lines = lines.filtered(lambda r: r.date == move_date)
            date_accounts = lines.mapped('account_id')
            for date_account in date_accounts:
                m_03 = []
                m_04 = []
                try:
                    # 1-3
                    m_03.extend([
                        move_date.strftime('%Y%m%d'),
                        date_account.code.rstrip('0'),
                        date_account.name,
                    ])
                    # 4-9
                    m_03.extend(['01', '', '', '', '1', ''])
                except:
                    m_03 = []
                if m_03:
                    lines_to_write_03.append('|'.join(m_03))
                if m_03:
                    # 1-3
                    m_04.extend(m_03[0:3])
                    # 4-9
                    m_04.extend(m_03[3:])
                if m_04:
                    lines_to_write_04.append('|'.join(m_04))
        for move in lines:
            m_01 = []
            m_02 = []
            try:
                serie = move.move_id.l10n_pe_edi_serie
                number = move.move_id.l10n_pe_edi_number
                if serie and number:
                    sunat_number = [serie, number]
                else:
                    sunat_number = ['', '']
                sunat_partner_code = move.move_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
                sunat_partner_vat = move.move_id.partner_id.vat
                move_id = move.id
                move_name = move.name
                if move_name:
                    move_name = move_name.replace(
                        '\r', ' ').replace('\n', ' ').split()
                    move_name = ' '.join(move_name)
                if not move_name:
                    move_name = 'Movimiento'
                move_name = move_name[:200].strip()
                date = move.date
                # 1-4
                m_01.extend([
                    date.strftime('%Y%m00'),
                    move.move_id.seat_number or '',
                    ('M'+str(move_id).rjust(9, '0')),
                    move.account_id.code.rstrip('0'),
                ])
                # 5-6
                m_01.extend(['', ''])
                # 7
                # m_01.append(move.always_set_currency_id.name)
                m_01.append(move.currency_id.name)
                # 8-9
                if sunat_partner_code and sunat_partner_vat:
                    m_01.extend([
                        sunat_partner_code,
                        sunat_partner_vat,
                    ])
                else:
                    m_01.extend(['', ''])
                # 10
                m_01.append(
                    (move.move_id.l10n_latam_document_type_id.code or ''))
                # 11-12
                m_01.extend(sunat_number)
                # 13-14
                m_01.extend([date.strftime('%d/%m/%Y'), ''])
                # 15
                m_01.append(date.strftime('%d/%m/%Y'))
                # 16-17
                m_01.extend([
                    move_name,
                    '',
                ])
                # 18-20
                m_01.extend([format(move.debit, '.2f'),
                             format(move.credit, '.2f'), ''])
                # 21-22
                m_01.extend(['1', ''])
            except:
                m_01 = []
            if m_01:
                # 1-4
                m_02.extend(m_01[0:4])
                # 5-6
                m_02.extend(m_01[4:6])
                # 7
                m_02.append(m_01[6])
                # 8-9
                m_02.extend(m_01[7:9])
                # 10
                m_02.append(m_01[9])
                # 11-12
                m_02.extend(m_01[10:12])
                # 13-14
                m_02.extend(m_01[12:14])
                # 15
                m_02.append(m_01[14])
                # 16-17
                m_02.extend(m_01[15:17])
                # 18-20
                m_02.extend(m_01[17:20])
                # 21-22
                m_02.extend(m_01[20:])
            if m_01:
                lines_to_write_01.append('|'.join(m_01))
            if m_02:
                lines_to_write_02.append('|'.join(m_02))
        name_01 = self.get_default_filename(
            ple_id='050100', empty=bool(lines_to_write_01))
        lines_to_write_01.append('')
        txt_string_01 = '\r\n'.join(lines_to_write_01)
        dict_to_write = dict()
        if txt_string_01:
            headers = [
                'Periodo',
                'Código Único de la Operación (CUO)',
                'Número correlativo del asiento contable',
                'Código de la cuenta contable desagregado en subcuentas al nivel máximo de dígitos utilizado',
                'Código de la Unidad de Operación, de la Unidad Económica Administrativa, de la Unidad de Negocio, de la Unidad de Producción, de la Línea, de la Concesión, del Local o del Lote',
                'Código del Centro de Costos, Centro de Utilidades o Centro de Inversión',
                'Tipo de Moneda de origen',
                'Tipo de documento de identidad del emisor',
                'Número de documento de identidad del emisor',
                'Tipo de Comprobante de Pago o Documento asociada a la operación',
                'Número de serie del comprobante de pago o documento asociada a la operación',
                'Número del comprobante de pago o documento asociada a la operación',
                'Fecha contable',
                'Fecha de vencimiento',
                'Fecha de la operación o emisión',
                'Glosa o descripción de la naturaleza de la operación registrada',
                'Glosa referencial',
                'Movimientos del Debe',
                'Movimientos del Haber',
                'Código del libro, campo 1, campo 2 y campo 3 del Registro de Ventas e Ingresos o del Registro de Compras',
                'Indica el estado de la operación',
            ]
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                txt_string_01, name_01[2:], headers=headers)
            dict_to_write.update({
                'ple_txt_01': txt_string_01,
                'ple_txt_01_binary': base64.b64encode(txt_string_01.encode()),
                'ple_txt_01_filename': name_01 + '.txt',
                'ple_xls_01_binary': xlsx_file_base_64.encode(),
                'ple_xls_01_filename': name_01 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_01': False,
                'ple_txt_01_binary': False,
                'ple_txt_01_filename': False,
                'ple_xls_01_binary': False,
                'ple_xls_01_filename': False,
            })
        name_03 = self.get_default_filename(
            ple_id='050300', empty=bool(lines_to_write_03))
        lines_to_write_03.append('')
        txt_string_03 = '\r\n'.join(lines_to_write_03)
        if txt_string_03:
            headers = [
                'Periodo',
                'Código de la Cuenta Contable desagregada hasta el nivel máximo de dígitos utilizado',
                'Descripción de la Cuenta Contable desagregada al nivel máximo de dígitos utilizado',
                'Código del Plan de Cuentas utilizado por el deudor tributario',
                'Descripción del Plan de Cuentas utilizado por el deudor tributario',
                'Código de la Cuenta Contable Corporativa desagregada hasta el nivel máximo de dígitos utilizado',
                'Descripción de la Cuenta Contable Corporativa desagregada al nivel máximo de dígitos utilizado',
                'Indica el estado de la operación',
            ]
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                txt_string_03, name_03[2:], headers=headers)
            dict_to_write.update({
                'ple_txt_03': txt_string_03,
                'ple_txt_03_binary': base64.b64encode(txt_string_03.encode()),
                'ple_txt_03_filename': name_03 + '.txt',
                'ple_xls_03_binary': xlsx_file_base_64.encode(),
                'ple_xls_03_filename': name_03 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_03': False,
                'ple_txt_03_binary': False,
                'ple_txt_03_filename': False,
                'ple_xls_03_binary': False,
                'ple_xls_03_filename': False,
            })
        name_02 = self.get_default_filename(
            ple_id='050200', empty=bool(lines_to_write_02))
        lines_to_write_02.append('')
        txt_string_02 = '\r\n'.join(lines_to_write_02)
        if txt_string_02:
            headers = [
                'Periodo',
                'Código Único de la Operación (CUO)',
                'Número correlativo del asiento contable',
                'Código de la cuenta contable desagregado en subcuentas al nivel máximo de dígitos utilizado',
                'Código de la Unidad de Operación, de la Unidad Económica Administrativa, de la Unidad de Negocio, de la Unidad de Producción, de la Línea, de la Concesión, del Local o del Lote',
                'Código del Centro de Costos, Centro de Utilidades o Centro de Inversión',
                'Tipo de Moneda de origen',
                'Tipo de documento de identidad del emisor',
                'Número de documento de identidad del emisor',
                'Tipo de Comprobante de Pago o Documento asociada a la operación',
                'Número de serie del comprobante de pago o documento asociada a la operación',
                'Número del comprobante de pago o documento asociada a la operación',
                'Fecha contable',
                'Fecha de vencimiento',
                'Fecha de la operación o emisión',
                'Glosa o descripción de la naturaleza de la operación registrada',
                'Glosa referencial',
                'Movimientos del Debe',
                'Movimientos del Haber',
                'Código del libro, campo 1, campo 2 y campo 3 del Registro de Ventas e Ingresos o del Registro de Compras',
                'Indica el estado de la operación',
            ]
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                txt_string_02, name_02[2:], headers=headers)
            dict_to_write.update({
                'ple_txt_02': txt_string_02,
                'ple_txt_02_binary': base64.b64encode(txt_string_02.encode()),
                'ple_txt_02_filename': name_02 + '.txt',
                'ple_xls_02_binary': xlsx_file_base_64.encode(),
                'ple_xls_02_filename': name_02 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_02': False,
                'ple_txt_02_binary': False,
                'ple_txt_02_filename': False,
                'ple_xls_02_binary': False,
                'ple_xls_02_filename': False,
            })
        name_04 = self.get_default_filename(
            ple_id='050400', empty=bool(lines_to_write_04))
        lines_to_write_04.append('')
        txt_string_04 = '\r\n'.join(lines_to_write_04)
        if txt_string_04:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(txt_string_04, name_04[2:], headers=[
                'Periodo',
                'Código de la Cuenta Contable desagregada hasta el nivel máximo de dígitos utilizado',
                'Descripción de la Cuenta Contable desagregada al nivel máximo de dígitos utilizado',
                'Código del Plan de Cuentas utilizado por el deudor tributario',
                'Descripción del Plan de Cuentas utilizado por el deudor tributario',
                'Código de la Cuenta Contable Corporativa desagregada hasta el nivel máximo de dígitos utilizado',
                'Descripción de la Cuenta Contable Corporativa desagregada al nivel máximo de dígitos utilizado',
                'Indica el estado de la operación',
            ])
            dict_to_write.update({
                'ple_txt_04': txt_string_04,
                'ple_txt_04_binary': base64.b64encode(txt_string_04.encode()),
                'ple_txt_04_filename': name_04 + '.txt',
                'ple_xls_04_binary': xlsx_file_base_64.encode(),
                'ple_xls_04_filename': name_04 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_04': False,
                'ple_txt_04_binary': False,
                'ple_txt_04_filename': False,
                'ple_xls_04_binary': False,
                'ple_xls_04_filename': False,
            })
        dict_to_write.update({
            'date_generated': str(fields.Datetime.now()),
        })
        res = self.write(dict_to_write)
        return res
