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

class PLEReport08(models.Model) :
	_name = 'ple.report.08'
	_description = 'PLE 08 - Estructura del Registro de Compras'
	_inherit = 'ple.report.templ'
	
	year = fields.Integer(required=True)
	month = fields.Selection(selection_add=[], required=True)
	
	bill_ids = fields.Many2many(comodel_name='account.move', string='Compras', readonly=True)
	
	ple_txt_01 = fields.Text(string='Contenido del TXT 8.1')
	ple_txt_01_binary = fields.Binary(string='TXT 8.1')
	ple_txt_01_filename = fields.Char(string='Nombre del TXT 8.1')
	ple_xls_01_binary = fields.Binary(string='Excel 8.1')
	ple_xls_01_filename = fields.Char(string='Nombre del Excel 8.1')
	ple_txt_03 = fields.Text(string='Contenido del TXT 8.3')
	ple_txt_03_binary = fields.Binary(string='TXT 8.3', readonly=True)
	ple_txt_03_filename = fields.Char(string='Nombre del TXT 8.3')
	ple_xls_03_binary = fields.Binary(string='Excel 8.3', readonly=True)
	ple_xls_03_filename = fields.Char(string='Nombre del Excel 8.3')
	
	def get_default_filename(self, ple_id='080100', empty=False) :
		name = super().get_default_filename()
		name_dict = {
			'month': str(self.month).rjust(2,'0'),
			'ple_id': ple_id,
		}
		if empty :
			name_dict.update({
				'contenido': '0',
			})
		fill_name_data(name_dict)
		name = name % name_dict
		return name
	
	def update_report(self) :
		res = super().update_report()
		start = datetime.date(self.year, int(self.month), 1)
		end = get_last_day(start)
		#current_offset = fields.Datetime.context_timestamp(self, fields.Datetime.now()).utcoffset()
		#start = start - current_offset
		#end = end - current_offset
		bills = self.env.ref('base.pe').id
		bills = [
			('company_id','=',self.company_id.id),
			('company_id.partner_id.country_id','=',bills),
			('move_type','in',['in_invoice','in_refund']),
			('state','=','posted'),
			('invoice_date','>=',str(start)),
			('invoice_date','<=',str(end)),
		]
		bills = self.env[self.bill_ids._name].search(bills, order='invoice_date asc, ref asc')
		self.bill_ids = bills
		return res
	
	def generate_report(self) :
		res = super().generate_report()
		lines_to_write_01 = []
		lines_to_write_03 = []
		bills = self.bill_ids.sudo()
		peru = self.env.ref('base.pe')
		for move in bills :
			m_01 = []
			try :
				sunat_number = move.ref
				sunat_number = sunat_number and ('-' in sunat_number) and sunat_number.split('-') or ['','']
				sunat_code = move.pe_invoice_code or '00'
				sunat_partner_code = move.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
				sunat_partner_vat = move.partner_id.vat
				sunat_partner_name = move.partner_id.legal_name or move.partner_id.name
				move_id = move.id
				invoice_date = move.invoice_date
				date_due = move.invoice_date_due
				amount_untaxed = move.amount_untaxed
				amount_tax = move.amount_tax
				amount_total = move.amount_total
				#1-4
				#m_01.extend([periodo.strftime('%Y%m00'), str(number), ('A'+str(number).rjust(9,'0')), invoice.invoice_date.strftime('%d/%m/%Y')])
				m_01.extend([
					invoice_date.strftime('%Y%m00'),
					str(move_id),
					('M'+str(move_id).rjust(9,'0')),
					invoice_date.strftime('%d/%m/%Y'),
				])
				#5
				if date_due :
					m_01.append(date_due.strftime('%d/%m/%Y'))
				else :
					m_01.append('')
				#6-10
				m_01.extend([
					sunat_code,
					sunat_number[0],
					'',
					sunat_number[1],
					'',
				])
				#11-13
				if sunat_partner_code and sunat_partner_vat and sunat_partner_name :
					m_01.extend([
						sunat_partner_code,
						sunat_partner_vat,
						sunat_partner_name,
					])
				else :
					m_01.extend(['', '', ''])
				#14-15
				m_01.extend([format(amount_untaxed, '.2f'), format(amount_tax, '.2f')])
				#16-23
				m_01.extend(['', '', '', '', '', '', '0.00', '']) #ICBP
				#24-26
				m_01.extend([format(amount_total, '.2f'), '', ''])
				#27-31
				if sunat_code in ['07', '08'] :
					"""origin = (sunat_code == '07') and move.credit_origin_id or move.debit_origin_id
					origin_number = origin.ref
					origin_number = origin_number and ('-' in origin_number) and origin_number.split('-') or ['', '']"""
					#m_01.extend([origin.invoice_date.strftime('%d/%m/%Y'), origin.pe_invoice_code])
					m_01.extend(["01/07/2021", "01"])
					#m_01.extend([origin_number[0], '', origin_number[1]])
					m_01.extend(['FC00', '', '00000001'])
				else :
					m_01.extend(['', '', '', '', ''])
				#32-43
				m_01.extend(['', '', '', '', '', '', '', '', '', '', '1', ''])
			except :
				_logging.info('error en lineaaaaaaaaaaaaaa 1754')
				m_01 = []
			if m_01 :
				lines_to_write_01.append('|'.join(m_01))
			m_03 = []
			if m_01 and (move.partner_id.country_id != peru) :
				#1-4
				#m_03.extend([
				#    invoice_date.strftime('%Y%m00'),
				#    str(move_id),
				#    ('A'+str(move_id).rjust(9,'0')),
				#    invoice_date.strftime('%d/%m/%Y'),
				#])
				m_03.extend(m_01[0:4])
				#5
				#if date_due :
				#    m_03.append(date_due.strftime('%d/%m/%Y'))
				#else :
				#    m_03.append('')
				m_03.append(m_01[4])
				#6-9
				#m_03.extend([
				#    sunat_code,
				#    sunat_number[0],
				#    sunat_number[1],
				#    '',
				#])
				m_03.extend([
					m_01[5],
					m_01[6],
					m_01[8],
				])
				#10-12
				#if sunat_partner_code and sunat_partner_vat and sunat_partner_name :
				#    m_03.extend([
				#        sunat_partner_code,
				#        sunat_partner_vat,
				#        sunat_partner_name,
				#    ])
				#else :
				#    m_03.extend(['', '', ''])
				m_03.extend(m_01[10:13])
				#13-14
				#m_03.extend([format(amount_untaxed, '.2f'), format(amount_tax, '.2f')])
				m_03.extend(m_01[13:15])
				#15
				#m_03.append('0.00') #ICBP
				m_03.append(m_01[21]) #ICBP
				#16-19
				#m_03.extend(['', format(amount_total, '.2f'), '', ''])
				m_03.extend(m_01[22:26])
				#20-23
				#if sunat_code in ['07', '08'] :
				#    origin = (sunat_code == '07') and move.credit_origin_id or move.debit_origin_id
				#    origin_number = origin.ref.split('-')
				#    m_03.extend([origin.invoice_date.strftime('%d/%m/%Y'), origin.pe_invoice_code])
				#    m_03.extend([origin_number[0], origin_number[1]])
				#else :
				#    m_03.extend(['', '', '', '', ''])
				m_03.extend([
					m_01[26],
					m_01[27],
					m_01[28],
					m_01[30],
				])
				#24-33
				#m_03.extend(['', '', '', '', '', '', '', '', '1', ''])
				m_03.extend(m_01[31:35]+m_01[36:39]+m_01[40:])
			if m_03 :
				lines_to_write_03.append('|'.join(m_03))
		name_01 = self.get_default_filename(ple_id='140100', empty=bool(lines_to_write_01))
		lines_to_write_01.append('')
		txt_string_01 = '\r\n'.join(lines_to_write_01)
		dict_to_write = dict()
		if txt_string_01 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(txt_string_01, name_01[2:], headers=[
				'Periodo',
				'Número correlativo del mes o Código Único de la Operación (CUO)',
				'Número correlativo del asiento contable',
				'Fecha de emisión del comprobante de pago o documento',
				'Fecha de Vencimiento o Fecha de Pago',
				'Tipo de Comprobante de Pago o Documento',
				'Serie del comprobante de pago o documento o código de la dependencia Aduanera',
				'Año de emisión de la DUA o DSI',
				'Número del comprobante de pago o documento o número de orden del formulario físico o virtual o número final',
				'Número final',
				'Tipo de Documento de Identidad del proveedor',
				'Número de RUC del proveedor o número de documento de Identidad',
				'Apellidos y nombres, denominación o razón social del proveedor',
				'Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas exclusivamente a operaciones gravadas y/o de exportación',
				'Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal',
				'Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas a operaciones gravadas y/o de exportación y a operaciones no gravadas',
				'Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal',
				'Base imponible de las adquisiciones gravadas que no dan derecho a crédito fiscal y/o saldo a favor por exportación, por no estar destinadas a operaciones gravadas y/o de exportación',
				'Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal',
				'Valor de las adquisiciones no gravadas',
				'Monto del Impuesto Selectivo al Consumo en los casos en que el sujeto pueda utilizarlo como deducción',
				'Impuesto al Consumo de las Bolsas de Plástico',
				'Otros conceptos, tributos y cargos que no formen parte de la base imponible',
				'Importe total de las adquisiciones registradas según comprobante de pago',
				'Código de la Moneda',
				'Tipo de cambio',
				'Fecha de emisión del comprobante de pago que se modifica',
				'Tipo de comprobante de pago que se modifica',
				'Número de serie del comprobante de pago que se modifica',
				'Código de la dependencia Aduanera de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI)',
				'Número del comprobante de pago que se modifica',
				'Fecha de emisión de la Constancia de Depósito de Detracción',
				'Número de la Constancia de Depósito de Detracción',
				'Marca del comprobante de pago sujeto a retención',
				'Clasificación de los bienes y servicios adquiridos',
				'Identificación del Contrato o del proyecto',
				'Error tipo 1: inconsistencia en el tipo de cambio',
				'Error tipo 2: inconsistencia por proveedores no habidos',
				'Error tipo 3: inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV',
				'Error tipo 4: inconsistencia por DNIs que fueron utilizados en las Liquidaciones de Compra y que ya cuentan con RUC',
				'Indicador de Comprobantes de pago cancelados con medios de pago',
				'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste',
			])
			dict_to_write.update({
				'ple_txt_01': txt_string_01,
				'ple_txt_01_binary': base64.b64encode(txt_string_01.encode()),
				'ple_txt_01_filename': name_01 + '.txt',
				'ple_xls_01_binary': xlsx_file_base_64.encode(),
				'ple_xls_01_filename': name_01 + '.xlsx',
			})
		else :
			dict_to_write.update({
				'ple_txt_01': False,
				'ple_txt_01_binary': False,
				'ple_txt_01_filename': False,
				'ple_xls_01_binary': False,
				'ple_xls_01_filename': False,
			})
		name_03 = self.get_default_filename(ple_id='140300', empty=bool(lines_to_write_03))
		lines_to_write_03.append('')
		txt_string_03 = '\r\n'.join(lines_to_write_03)
		if txt_string_03 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(txt_string_03, name_03[2:], headers=[
				'Periodo',
				'Número correlativo del mes o Código Único de la Operación (CUO)',
				'Número correlativo del asiento contable',
				'Fecha de emisión del comprobante de pago o documento',
				'Fecha de Vencimiento o Fecha de Pago',
				'Tipo de Comprobante de Pago o Documento',
				'Serie del comprobante de pago o documento o código de la dependencia Aduanera',
				'Número del comprobante de pago o documento o número de orden del formulario físico o virtual o número final',
				'Número final',
				'Tipo de Documento de Identidad del proveedor',
				'Número de RUC del proveedor o número de documento de Identidad',
				'Apellidos y nombres, denominación o razón social del proveedor',
				'Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas exclusivamente a operaciones gravadas y/o de exportación',
				'Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal',
				'Impuesto al Consumo de las Bolsas de Plástico',
				'Otros conceptos, tributos y cargos que no formen parte de la base imponible',
				'Importe total de las adquisiciones registradas según comprobante de pago',
				'Código de la Moneda',
				'Tipo de cambio',
				'Fecha de emisión del comprobante de pago que se modifica',
				'Tipo de comprobante de pago que se modifica',
				'Número de serie del comprobante de pago que se modifica',
				'Número del comprobante de pago que se modifica',
				'Fecha de emisión de la Constancia de Depósito de Detracción',
				'Número de la Constancia de Depósito de Detracción',
				'Marca del comprobante de pago sujeto a retención',
				'Clasificación de los bienes y servicios adquiridos',
				'Error tipo 1: inconsistencia en el tipo de cambio',
				'Error tipo 2: inconsistencia por proveedores no habidos',
				'Error tipo 3: inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV',
				'Indicador de Comprobantes de pago cancelados con medios de pago',
				'Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste',
			])
			dict_to_write.update({
				'ple_txt_03': txt_string_03,
				'ple_txt_03_binary': base64.b64encode(txt_string_03.encode()),
				'ple_txt_03_filename': name_03 + '.txt',
				'ple_xls_03_binary': xlsx_file_base_64.encode(),
				'ple_xls_03_filename': name_03 + '.xlsx',
			})
		else :
			dict_to_write.update({
				'ple_txt_03': False,
				'ple_txt_03_binary': False,
				'ple_txt_03_filename': False,
				'ple_xls_03_binary': False,
				'ple_xls_03_filename': False,
			})
		dict_to_write.update({
			'date_generated': str(fields.Datetime.now()),
		})
		res = self.write(dict_to_write)
		return res
