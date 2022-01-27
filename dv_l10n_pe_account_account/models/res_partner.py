from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # NO domiciliados
    l10n_pe_is_non_domiciled = fields.Boolean(string='No domiciliado')
    l10n_pe_partner_country_id = fields.Many2one(
        'res.country', string='Pais de residencia del no domiciliado')
    l10n_pe_partner_street = fields.Char(string='Domicilio en el extranjero')
    l10n_pe_partner_vat = fields.Char(string='Documento de identidad')

    @api.constrains('vat')
    def constrains_vat(self):
        if self.l10n_latam_identification_type_id.l10n_pe_vat_code == '6' and len(self.vat) != 11:
            raise ValidationError(
                'El RUC debe ser de 11 digitos.')
        elif self.l10n_latam_identification_type_id.l10n_pe_vat_code == '1' and len(self.vat) != 8:
            raise ValidationError(
                'El DNI debe ser de 8 digitos.')
