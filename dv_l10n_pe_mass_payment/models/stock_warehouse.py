from odoo import api, fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    payment_internal_code = fields.Char(string='Código interno de pago Telecrédito')