import base64
import xlwt
import platform
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class PleReport(models.Model):
    _name = 'ple.report'
    _description = 'Plantilla Reporte Ple'
    name = fields.Char(string='Periodo', compute='_compute_name')

    def convert_field_to_string(self, field):
        if field:
            string_field = str(field)
        else:
            string_field = ''
        return string_field

    @api.depends('start_date', 'finish_date')
    def _compute_name(self):
        for record in self:
            if record.start_date and record.finish_date:
                name = f"{record.start_date} {record.finish_date}"
            elif record.start_date:
                name = f"{record.start_date}"
            elif record.finish_date:
                name = f"{record.finish_date}"
            else:
                name = 'Nuevo periodo'
            record.name = name

    company_id = fields.Many2one(
        comodel_name='res.company', string='Compañía', required=True)
    start_date = fields.Date(string='Fecha Inicio', required=True)
    start_date_year = fields.Char(
        string='Año de inicio del reporte', compute='_compute_date_format', store=True)
    start_date_month = fields.Char(
        string='Mes de inicio del reporte', compute='_compute_date_format', store=True)
    finish_date = fields.Date(string='Fecha Fin', required=True)
    finish_date_year = fields.Char(
        string='Año de término del reporte', compute='_compute_date_format', store=True)
    finish_date_month = fields.Char(
        string='Mes de término del reporte', compute='_compute_date_format', store=True)

    @api.depends('start_date', 'finish_date')
    def _compute_date_format(self):
        for record in self:
            start_date = datetime.strptime(str(record.start_date), '%Y-%m-%d')
            finish_date = datetime.strptime(
                str(record.finish_date), '%Y-%m-%d')

            start_date_year = start_date.strftime('%Y')
            start_date_month = start_date.strftime('%m')
            finish_date_year = finish_date.strftime('%Y')
            finish_date_month = finish_date.strftime('%m')

            record.write({
                'start_date_year': start_date_year,
                'start_date_month': start_date_month,
                'finish_date_year': finish_date_year,
                'finish_date_month': finish_date_month,
            })

    report_state = fields.Selection(string='Estado de envío', selection=[
        ('draft', 'Borrador'),
        ('created', 'Generado'),
        ('declarated', 'Declarado')],default='draft')
    txt_creation_datetime = fields.Datetime(
        string='Fecha de generación de TXT', readonly=True)
    xls_creation_datetime = fields.Datetime(
        string='Fecha de generación de XLS', readonly=True)

    def action_declare(self):
        self.report_state = 'declarated'

    def action_draft(self):
        self.report_state = 'draft'

    emission_state = fields.Selection([
        ('operations', 'Cierre de Operaciones - Bajo de inscripciones e el RUC'),
        ('enterprise', 'Empresa o Entidad Operativa'),
        ('close', 'Cierre del libro - No obligado a llevarlo'),
    ], string='Estado de envio', default='enterprise')

    emission_state_code = fields.Char(
        string='Codigo de envio', compute='_compute_emission_state_code', store=True)

    @api.depends('emission_state')
    def _compute_emission_state_code(self):
        for record in self:
            emission_state = record.emission_state
            if emission_state == 'operations':
                emission_state_code = '0'
            elif emission_state == 'enterprise':
                emission_state_code = '1'
            elif emission_state == 'close':
                emission_state_code = '2'
            record.emission_state_code = emission_state_code

    def validate_date_filters(self):
        for record in self:
            if record.end_date and record.end_date < record.start_date:
                record.end_date = False
                raise ValidationError(
                    'La fecha fin debe ser mayor a la fecha de inicio.')
            elif record.start_date_year != record.finish_date_year:
                record.end_date = False
                raise ValidationError(
                    'El reporte debe ser de un mismo año.')

    def _get_content_code(self,report_format='8_1'):
        if self._get_periord_format_report_invoice_ids(report_format):
            content_code = '1'
        else:
            content_code = '0'
        return content_code

    def _get_report_period(self):
        if self.start_date_month == self.finish_date_month:
            report_period = f'{self.start_date_year}{self.start_date_month}00'
        else:
            report_period = f'{self.start_date_year}0000'
        return report_period

    def _generate_ple_filename(self, report_format='8_1', file_format='.txt'):
        ruc = self.company_id.vat
        report_period = self._get_report_period()
        if report_format == '8_1':
            report_identification = '080100'
        elif report_format == '8_2':
            report_identification = '080200'
        elif report_format == '8_3':
            report_identification = '080300'
        elif report_format == '14_1':
            report_identification = '140100'
        elif report_format == '14_2':
            report_identification = '140200'
        oportunity_code = '00'
        emission_state_code = self.emission_state_code
        content_code = self._get_content_code(report_format)
        currency = '1'
        filename = f"LE{ruc}{report_period}{report_identification}{oportunity_code}{emission_state_code}{content_code}{currency}1{file_format}"
        return filename

    def _get_periord_format_report_invoice_ids(self,report_format='8_1'):
        period_invoice_ids = self.period_invoice_ids
        return period_invoice_ids
    
    def generate_ple_txt_file(self, report_format='8_1'):
        for record in self:
            str_line = ''
            for acc_mov in self._get_periord_format_report_invoice_ids(report_format):
                for field in acc_mov.get_report_format_fields(report_format,acc_mov.state):
                    _logger.info(field)
                    field = self.convert_field_to_string(field)
                    str_line += field + '|'
                str_line += '\n'

            record.write({
                f'ple_{report_format}_txt_filename': record._generate_ple_filename(report_format, '.txt'),
                f'ple_{report_format}_txt_file': base64.b64encode(str_line.encode("utf-8"))
            })

    def generate_ple_xls_file(self, report_format='8_1'):
        for record in self:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet(report_format)
            sheet = self.write_report_format_header(sheet,report_format)
            row = 1
            for acc_mov in self._get_periord_format_report_invoice_ids(report_format):
                column = 0
                for field in acc_mov.get_report_format_fields(report_format,acc_mov.state):
                    field = self.convert_field_to_string(field)
                    sheet.write(row, column, field)
                    column += 1
                row += 1

            if platform.system() == 'Linux':
                filename = ('/tmp/ple_report' + '.xls')
            else:
                filename = ('ple_report' + '.xls')
            workbook.save(filename)
            fp = open(filename, "rb")
            file_data = fp.read()

            record.write({
                f'ple_{report_format}_xls_filename': record._generate_ple_filename(report_format, '.xls'),
                f'ple_{report_format}_xls_file': base64.b64encode(file_data)
            })
    
    def _write_ple_8_1_excel_header(self, sheet):
        sheet.write(0, 0, 'Periodo')
        sheet.write(0, 1, 'CUO')
        sheet.write(0, 2, 'Número correlativo del asiento contable')
        sheet.write(0, 3, 'Fecha de emisión')
        sheet.write(0, 4, 'Fecha de Vencimiento')
        sheet.write(0, 5, 'Tipo de Comprobante')
        sheet.write(0, 6, 'Numero de serie.')
        sheet.write(0, 7, 'Año de emisión de la DUA o DSI.')
        sheet.write(0, 8, 'Correlativo')
        sheet.write(0, 9, 'En caso de optar por anotar el importe total de las operaciones diarias que no otorguen derecho a crédito fiscal en forma consolidada, registrar el número final (2).')
        sheet.write(0, 10, 'Tipo de Documento de Identidad del proveedor.')
        sheet.write(0, 11, 'Número de documento de Identidad.')
        sheet.write(0, 12, 'Razón social.')
        sheet.write(0, 13, 'Base imponible.')
        sheet.write(0, 14, 'IGV.')
        sheet.write(0, 15, 'Base imponible.')
        sheet.write(0, 16, 'IGV.')
        sheet.write(0, 17, 'Base imponible.')
        sheet.write(0, 18, 'IGV.')
        sheet.write(0, 19, 'Valor de las adquisiciones no gravadas')                        
        sheet.write(0, 20, 'ISC')
        sheet.write(0, 21, 'Impuesto al Consumo de las Bolsas de Plástico')
        sheet.write(0, 22, 'Otros conceptos, tributos y cargos que no formen parte de la base imponible')
        sheet.write(
            0, 23, 'Importe total de las adquisiciones registradas según comprobante de pago')
        sheet.write(0, 24, 'Código  de la Moneda (Tabla 4)')
        sheet.write(0, 25, 'Tipo de cambio (5)')
        sheet.write(0, 26, 'NC-ND: Fecha emision')
        sheet.write(0, 27, 'NC-ND: Tipo de comprobante')
        sheet.write(0, 28, 'NC-ND: Numero de serie')
        sheet.write(0, 29, 'Código de la dependencia Aduanera de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI) .')
        sheet.write(0, 30, 'NC-ND: Correlativo')
        sheet.write(
            0, 31, 'Fecha de emisión de la Constancia de Depósito de Detracción (6)')
        sheet.write(
            0, 32, 'Número de la Constancia de Depósito de Detracción (6)')
        sheet.write(0, 33, 'Marca del comprobante de pago sujeto a retención')
        sheet.write(
            0, 34, 'Clasificación de los bienes y servicios adquiridos (Tabla 30) - mayor a 1 500 UIT')
        sheet.write(0, 35, 'Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, consorcios, joint ventures u otras formas de contratos de colaboración empresarial, que no lleven contabilidad independiente.')
        sheet.write(0, 36, 'Error tipo 1: inconsistencia en el tipo de cambio')
        sheet.write(
            0, 37, 'Error tipo 2: inconsistencia por proveedores no habidos')
        sheet.write(
            0, 38, 'Error tipo 3: inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV')
        sheet.write(
            0, 39, 'Error tipo 4: inconsistencia por DNIs que fueron utilizados en las Liquidaciones de Compra y que ya cuentan con RUC')
        sheet.write(
            0, 40, 'Indicador de Comprobantes de pago cancelados con medios de pago')
        sheet.write(
            0, 41, 'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.')
        sheet.write(0, 42, 'Campos de libre utilización.')
        return sheet

   
    def _write_ple_8_2_excel_header(self, sheet):
        sheet.write(0, 0, 'Periodo')
        sheet.write(0, 1, 'CUO')
        sheet.write(0, 2, 'Número correlativo del asiento contable')
        sheet.write(0, 3, 'Fecha de emisión')
        sheet.write(0, 4, 'Tipo Tabla 10 Codigo de Boleta o Factura')
        sheet.write(0, 5, 'Serie')
        sheet.write(0, 6, 'Número correlativo del comprobante')
        sheet.write(0, 7, 'Valor de las adquisiciones')
        sheet.write(0, 8, 'Otros conceptos adicionales')
        sheet.write(
            0, 9, 'Importe total de las adquisiciones registradas según comprobante de pago o documento')
        sheet.write(
            0, 10, 'Tipo de Comprobante de Pago o Documento que sustenta el crédito fiscal')
        sheet.write(0, 11, 'Serie del comprobante de pago o documento que sustenta el crédito fiscal. En los casos de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI) se consignará el código de la dependencia Aduanera.')
        sheet.write(
            0, 12, 'Año de emisión de la DUA o DSI que sustenta el crédito fiscal')
        sheet.write(0, 13, 'Número del comprobante de pago o documento o número de orden del formulario físico o virtual donde conste el pago del impuesto, tratándose de la utilización de servicios prestados por no domiciliados u otros, número de la DUA o de la DSI, que sustente el crédito fiscal.')
        sheet.write(0, 14, 'Monto de retención del IGV')
        sheet.write(0, 15, 'Código  de la Moneda (Tabla 4)')
        sheet.write(0, 16, 'Tipo de cambio (5)')
        sheet.write(0, 17, 'Pais de la residencia del sujeto no domiciliado')
        sheet.write(0, 18, 'Apellidos y nombres, denominación o razón social  del sujeto no domiciliado. En caso de personas naturales se debe consignar los datos en el siguiente orden: apellido paterno, apellido materno y nombre completo.')
        sheet.write(
            0, 19, 'Domicilio en el extranjero del sujeto no domiciliado')
        sheet.write(0, 20, 'Número de identificación del sujeto no domiciliado')
        sheet.write(
            0, 21, 'Número de identificación fiscal del beneficiario efectivo de los pagos')
        sheet.write(0, 22, 'Apellidos y nombres, denominación o razón social  del beneficiario efectivo de los pagos. En caso de personas naturales se debe consignar los datos en el siguiente orden: apellido paterno, apellido materno y nombre completo.')
        sheet.write(
            0, 23, 'Pais de la residencia del beneficiario efectivo de los pagos')
        sheet.write(
            0, 24, 'Vínculo entre el contribuyente y el residente en el extranjero')
        sheet.write(0, 25, 'Renta Bruta')
        sheet.write(
            0, 26, 'Deducción / Costo de Enajenación de bienes de capital')
        sheet.write(0, 27, 'Renta Neta')
        sheet.write(0, 28, 'Tasa de retención')
        sheet.write(0, 29, 'Impuesto retenido')
        sheet.write(0, 30, 'Convenios para evitar la doble imposición')
        sheet.write(0, 31, 'Exoneración aplicada')
        sheet.write(0, 32, 'Tipo de Renta')
        sheet.write(
            0, 33, 'Modalidad del servicio prestado por el no domiciliado')
        sheet.write(
            0, 34, 'Aplicación del penultimo parrafo del Art. 76° de la Ley del Impuesto a la Renta')
        sheet.write(
            0, 35, 'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.')
        sheet.write(0, 36, 'Campos de libre utilización.')
        return sheet
    
    def _write_ple_8_3_excel_header(self, sheet):
        sheet.write(0, 0, 'Periodo')
        sheet.write(0, 1, 'CUO')
        sheet.write(0, 2, 'Número correlativo del asiento contable')
        sheet.write(0, 3, 'Fecha de emisión')
        sheet.write(0, 4, 'Fecha de Vencimiento')
        sheet.write(0, 5, 'Tipo de Comprobante')
        sheet.write(0, 6, 'Numero de serie')
        sheet.write(0, 7, 'Correlativo')
        sheet.write(
            0, 8, 'Total de las operaciones diarias que no otorguen derecho a crédito')
        sheet.write(0, 9, 'Tipo de Documento de Identidad del proveedor')
        sheet.write(0, 10, 'Número de documento de Identidad')
        sheet.write(0, 11, 'Razón social')
        sheet.write(0, 12, 'Base imponible')
        sheet.write(0, 13, 'IGV')
        sheet.write(0, 14, 'Otros tributos')
        sheet.write(0, 15, 'Importe total')
        sheet.write(0, 16, 'Codigo de la moneda')
        sheet.write(0, 17, 'Tipo de cambio')
        sheet.write(0, 18, 'NC-ND: Fecha emision')
        sheet.write(0, 19, 'NC-ND: Tipo de comprobante')
        sheet.write(0, 20, 'NC-ND: Numero de serie')
        sheet.write(0, 21, 'NC-ND: Correlativo')
        sheet.write(
            0, 22, 'Fecha de emisión de la Constancia de Depósito de Detracción (6)')
        sheet.write(
            0, 23, 'Número de la Constancia de Depósito de Detracción (6)')
        sheet.write(0, 24, 'Marca del comprobante de pago sujeto a retención')
        sheet.write(
            0, 25, 'Clasificación de los bienes y servicios adquiridos (Tabla 30) - mayor a 1 500 UIT')
        sheet.write(0, 26, 'Error tipo 1: inconsistencia en el tipo de cambio')
        sheet.write(
            0, 27, 'Error tipo 2: inconsistencia por proveedores no habidos')
        sheet.write(
            0, 28, 'Error tipo 3: inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV')
        sheet.write(
            0, 29, 'Indicador de Comprobantes de pago cancelados con medios de pago')
        sheet.write(
            0, 30, 'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.')
        sheet.write(0, 31, 'Campos de libre utilización.')
        return sheet

    def _write_ple_14_1_excel_header(self, sheet):
        sheet.write(0, 0, 'Periodo')
        sheet.write(0, 1, 'CUO')
        sheet.write(0, 2, 'Número correlativo del asiento contable')
        sheet.write(0, 3, 'Fecha de emisión')
        sheet.write(0, 4, 'Fecha de Vencimiento')
        sheet.write(0, 5, 'Tipo de Comprobante')
        sheet.write(0, 6, 'Numero de serie')
        sheet.write(0, 7, 'Correlativo')
        sheet.write(0, 8, 'Numero de ticket')
        sheet.write(0, 9, 'Tipo de Documento de Identidad del proveedor')
        sheet.write(0, 10, 'Número de documento de Identidad')
        sheet.write(0, 11, 'Razón social')
        sheet.write(0, 12, 'Valor facturado de la exportación')
        sheet.write(0, 13, 'Base imponible de la operación gravada')
        sheet.write(0, 14, 'Descuento de la base imponible')
        sheet.write(0, 15, 'IGV')
        sheet.write(0, 16, 'Descuento del IGV')
        sheet.write(0, 17, 'Importe total de la operación exonerada')
        sheet.write(0, 18, 'Importe total de la operación inafecta')
        sheet.write(0, 19, 'ISC')
        sheet.write(0, 20, 'Base imponible con IVAP')
        sheet.write(0, 21, 'IVAP')
        sheet.write(0, 22, 'ICBPER')
        sheet.write(0, 23, 'Otros tributos')
        sheet.write(0, 24, 'Importe total')
        sheet.write(0, 25, 'Codigo de la moneda')
        sheet.write(0, 26, 'Tipo de cambio')
        sheet.write(0, 27, 'NC-ND: Fecha emision')
        sheet.write(0, 28, 'NC-ND: Tipo de comprobante')
        sheet.write(0, 29, 'NC-ND: Numero de serie')
        sheet.write(0, 30, 'NC-ND: Correlativo')
        sheet.write(0, 31, 'Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, consorcios, joint ventures u otras formas de contratos de colaboración empresarial, que no lleven contabilidad independiente.')
        sheet.write(0, 32, 'Error tipo 1: inconsistencia en el tipo de cambio')
        sheet.write(
            0, 33, 'Indicador de Comprobantes de pago cancelados con medios de pago')
        sheet.write(
            0, 34, 'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.')
        sheet.write(0, 35, 'Campos de libre utilización.')
        return sheet
    
    def _write_ple_14_2_excel_header(self, sheet):
        sheet.write(0, 0, 'Periodo')
        sheet.write(0, 1, 'CUO')
        sheet.write(0, 2, 'Número correlativo del asiento contable')
        sheet.write(0, 3, 'Fecha de emisión')
        sheet.write(0, 4, 'Fecha de Vencimiento')
        sheet.write(0, 5, 'Tipo de Comprobante')
        sheet.write(0, 6, 'Numero de serie')
        sheet.write(0, 7, 'Correlativo')
        sheet.write(
            0, 8, 'Total de las operaciones diarias que no otorguen derecho a crédito')
        sheet.write(0, 9, 'Tipo de Documento de Identidad del proveedor')
        sheet.write(0, 10, 'Número de documento de Identidad')
        sheet.write(0, 11, 'Razón social')
        sheet.write(0, 12, 'Base imponible')
        sheet.write(0, 13, 'IGV')
        sheet.write(0, 14, 'Otros tributos')
        sheet.write(0, 15, 'Importe total')
        sheet.write(0, 16, 'Codigo de la moneda')
        sheet.write(0, 17, 'Tipo de cambio')
        sheet.write(0, 18, 'NC-ND: Fecha emision')
        sheet.write(0, 19, 'NC-ND: Tipo de comprobante')
        sheet.write(0, 20, 'NC-ND: Numero de serie')
        sheet.write(0, 21, 'NC-ND: Correlativo')
        sheet.write(0, 22, 'Error tipo 1: inconsistencia en el tipo de cambio')
        sheet.write(
            0, 23, 'Indicador de Comprobantes de pago cancelados con medios de pago')
        sheet.write(
            0, 24, 'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.')
        sheet.write(0, 25, 'Campos de libre utilización.')
        return sheet


    def write_report_format_header(self,sheet, report_format='8_1'):
        if report_format == '8_1':
            report_header = self._write_ple_8_1_excel_header(sheet)
        elif report_format == '8_2':
            report_header = self._write_ple_8_2_excel_header(sheet)
        elif report_format == '8_3':
            report_header = self._write_ple_8_3_excel_header(sheet)
        elif report_format == '14_1':
            report_header = self._write_ple_14_1_excel_header(sheet)
        elif report_format == '14_2':
            report_header = self._write_ple_14_2_excel_header(sheet)
        return report_header