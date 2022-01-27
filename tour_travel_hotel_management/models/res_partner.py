# See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_guide = fields.Boolean('Is Guide')
    service_ids = fields.One2many('guide.service',
                                  'partner_id',
                                  string='Services')

class GuideServices(models.Model):
    _name = 'guide.service'
    _description = "Guide Service"

    product_id = fields.Many2one('product.product', 'Services')
    unit_price = fields.Float('Unit Price')
    partner_id = fields.Many2one('res.partner', 'Guide')
