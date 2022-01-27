#  See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class VisaPackageLine(models.Model):
    _name = "visa.package.line"
    _description = 'Visa'

    name = fields.Text(translate=True)
    product_id = fields.Many2one('product.product', 'Visa')
    supplier_id = fields.Many2one('res.partner', 'Supplier')
    description = fields.Char('Description')
    visa_status = fields.Char('Visa Status')
    unit_price = fields.Float('Unit Price')
    cost_price = fields.Float('Cost Price')
    sale_order_templete_id = fields.Many2one('sale.order.template',
                                             string='Sale Order')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer()

    @api.onchange('product_id', 'cost_price')
    def onchange_product_id(self):
        if self.product_id:
            self.update({'unit_price': self.sale_order_templete_id._get_price_with_commission(self.product_id.standard_price),
                        'cost_price': self.product_id.standard_price})
