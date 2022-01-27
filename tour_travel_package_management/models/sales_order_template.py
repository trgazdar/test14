#  See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError
from docutils.nodes import line
import logging
_logger = logging.getLogger(__name__)

class SaleOrderTemplete(models.Model):
    _inherit = "sale.order.template"

    @api.onchange('meal_package_line_ids','meal_package_line_ids.qty','meal_package_line_ids.cost_price', 'transportation_package_line_ids','transportation_package_line_ids.qty','transportation_package_line_ids.cost_price', 'hotel_package_line_ids','hotel_package_line_ids.qty','hotel_package_line_ids.cost_price', 'extra_ticket_package_line_ids','extra_ticket_package_line_ids.qty','extra_ticket_package_line_ids.cost_price', 'ticket_package_line_ids','ticket_package_line_ids.qty','ticket_package_line_ids.cost_price')
    def get_amount_total_without_commission(self): 
        super(SaleOrderTemplete,self).get_amount_total_without_commission()