from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    l10n_pe_edi_table_13_id = fields.Many2one('l10n_pe_edi.table.13', string='Catálogo de existencias')
    l10n_pe_edi_table_13_code = fields.Char(related='l10n_pe_edi_table_13_id.code', string='Código')

    l10n_pe_edi_table_05_id = fields.Many2one('l10n_pe_edi.table.05', string='Tipo de existencia')
    l10n_pe_edi_table_05_code = fields.Char(related='l10n_pe_edi_table_05_id.code', string='Código')
    
    l10n_pe_edi_table_14_id = fields.Many2one('l10n_pe_edi.table.14', string='Método de valuación')
    l10n_pe_edi_table_14_code = fields.Char(related='l10n_pe_edi_table_14_id.code', string='Código')