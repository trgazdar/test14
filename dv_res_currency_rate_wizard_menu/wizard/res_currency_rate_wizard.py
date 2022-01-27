from odoo import api, fields, models


class CurrencyRate(models.TransientModel):
    _name = 'res.currency.rate.wizard'

    date = fields.Date(
        string='Fecha', default=fields.Date.context_today, required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moneda', required=True)
    company_id = fields.Many2one(
        'res.company', string='Compañía', default=lambda self: self.env.company, required=True)
    rate = fields.Float(string='Tipo de cambio', required=True)

    def create_currency_rate(self):
        currency_rate = self.env['res.currency.rate'].create({
            'name': self.date,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'rate': self.rate,
        })
        return currency_rate
