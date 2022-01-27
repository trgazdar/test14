from odoo import models, fields, api, _


class UomUom(models.Model):
    _inherit = 'uom.uom'

    l10n_pe_edi_table_06_id = fields.Many2one('l10n_pe_edi.table.06', string='Código de la unidad de medida')
    l10n_pe_edi_table_06_code = fields.Char(related='l10n_pe_edi_table_06_id.code', string='Código')