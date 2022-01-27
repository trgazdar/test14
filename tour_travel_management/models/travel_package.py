#  See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import logging
_logger = logging.getLogger(__name__)

class Country(models.Model):
    _inherit = 'res.country'
    _description = 'Country'
    _order = 'name'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        args = args or []
        context = dict(self._context) or {}
        if context.get('package_type'):
            if context.get('package_type') == 'international':
                args.append(('id', '!=', self.env.company.country_id.id))
            if context.get('package_type') == 'domestic':
                args.append(('id', '=', self.env.company.country_id.id))
        return super(Country, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)


class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    price_unit = fields.Float(
        'Unit Price', required=True, digits='Product Price')
    discount = fields.Float('Discount (%)', digits='Discount', default=0.0)


class TravelPackage(models.Model):
    _name = 'sale.order.template'
    _inherit = ['sale.order.template', 'mail.thread', 'mail.activity.mixin']
    _description = 'Tour Package'

    # Develogers Start
    amount_total_without_commission = fields.Float('Total sin comisión')
    commission_percentage = fields.Float('Porcentaje de Comisión')
    amount_total = fields.Float('Monto Total')
    
    def _get_price_with_commission(self, price):
        return price * (1 + (self.commission_percentage / 100))
    
    @api.onchange('commission_percentage','amount_total_without_commission')
    def onchange_commission_percentage(self):
        amount_total = self._get_price_with_commission(self.amount_total_without_commission)
        self.amount_total = amount_total
    
    def get_amount_total_without_commission(self):
        print("get amount total without commission base")
        _logger.info("get amount total without commission base")
        amount_total_without_commission = self.get_cost_price()
        self.amount_total_without_commission = amount_total_without_commission
    
    def action_generate_purchase_orders(self):
        vals = self._generate_purchase_order_vals()
        res = self.env['purchase.order'].create(vals)
        return res
    
    def _generate_purchase_order_vals(self):
        vals = []
        return vals
      
    # Develogers End
    @api.depends('arrival_date', 'return_date')
    def _compute_package_days(self):
        self.package_total_days = "0 Nights/ 0 Days"
        for package in self:
            if package.return_date and package.arrival_date:
                nights = ((package.return_date - package.arrival_date).
                          days)
                package.package_total_days = str(
                    nights) + ' ' + 'Nights' + ' ' + '/' + ' ' + \
                    str(nights + 1) + ' ' + 'Days'
                package.days = nights + 1
                package.nights = nights

    def compute_total_registration(self):
        self.total_registration = 0.0
        for package in self:
            confirm_reg = self.env['sale.order'].search_count(
                [('sale_order_template_id', '=', package.id)])
            package.total_registration = confirm_reg

    def get_cost_price(self):
        return 0.0

    def get_sell_price(self):
        return 0.0

    def _compute_cost_per_person(self):
        self.update({'cost_per_person': 0.0})

    def _compute_sell_per_person(self):
        self.update({'sell_per_person': 0.0})

    def get_grp_cost_price(self):
        return 0.0

    @api.depends('cost_per_person', 'sell_per_person')
    def _compute_profit_margin(self):
        self.profit_margin = 0.0
        for margin in self:
            if margin.cost_per_person and margin.sell_per_person:
                profit = margin.sell_per_person - margin.cost_per_person
                margin.update({'profit_margin': profit})

    def _compute_count_rfq(self):
        for package in self:
            purchase_orders = self.env['purchase.order'].search([
                ('package_id', 'in', [package.id])])
            package.rfq_count = len(purchase_orders)

    tour_number = fields.Char("Package Sequence",
                              readonly=True,
                              required=True,
                              copy=False,
                              default='New')
    arrival_date = fields.Date(
        'Arrival Date',
        copy=False,
        help='Expected date come to\
        a hotel or other location')
    return_date = fields.Date(
        'Departure Date',
        copy=False,
        help='Expected date to leave\
        a hotel or other location.')
    itinerary_ids = fields.One2many(
        'package.itinerary',
        'sale_order_template_id',
        'Itinerary',
        help='Package Itinerary')
    responsible_id = fields.Many2one(
        'res.users',
        'Responsible',
        default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        string='States',
        default='draft',
        tracking=True)
    category_id = fields.Many2one(
        'package.category',
        'Package Category', ondelete='restrict')
    package_type = fields.Selection([
        ('domestic', 'Domestic'),
        ('international', 'International')],
        string='Package Type',
        default='domestic')
    discription = fields.Html('Comments')
    country_id = fields.Many2one(
        'res.country',
        'Country',
        default=lambda self: self.env.user.company_id.country_id,
        index=True)
    state_id = fields.Many2one(
        'res.country.state',
        'State',
        index=True)
    pax_group = fields.Integer(
        'Minimum Travellers',
        help='Minimum Number of Persons participating in current package')
    max_pax_group = fields.Integer(
        'Maximum Travellers',
        help='Maximum Number of Persons participating in current package')
    package_total_days = fields.Char(
        'package Days/Nights',
        compute='_compute_package_days',
        store=True)
    days = fields.Char(
        'package Days',
        compute='_compute_package_days',
        store=True)
    nights = fields.Char(
        'package Nights',
        compute='_compute_package_days',
        store=True)
    is_package = fields.Boolean('Is Package')
    total_passenger = fields.Integer(
        'Total Passenger',
        compute='compute_total_passenger')
    total_registration = fields.Integer(
        'Total Registration',
        compute='compute_total_registration')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.company)
    cost_per_person = fields.Float(
        'Cost Per Person',
        compute='_compute_cost_per_person', store=True)
    sell_per_person = fields.Float(
        'Sell per Person',
        compute='_compute_sell_per_person', store=True)
    profit_type = fields.Selection([
        ('fixed', 'Fix Price'),
        ('percentage', 'Percentage (discount)')],
        string='Profit Type',
        index=True,
        default='fixed')
    profit_amount = fields.Float('Fixed Price')
    profit_margin = fields.Float('Margin', compute='_compute_profit_margin')
    rfq_count = fields.Integer('RFQ Count',
                               compute="_compute_count_rfq")
    selling_currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
        string='Selling Currency')
    name = fields.Text('Description', translate=True)
    group_costing_ids = fields.One2many('group.costing.line', 'sale_order_template_id',
                                        'Group Costing')

    @api.onchange('package_type')
    def _onchange_package_type(self):
        self.country_id = False
        if self.package_type == 'domestic':
            self.update({'country_id': self.env.company.country_id.id})

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.state_id = False

    @api.model
    def default_get(self, fields):
        res = super(TravelPackage, self).default_get(fields)
        category_id = self.env.context.get('active_id')
        if category_id:
            res['category_id'] = category_id
        return res

    @api.model
    def create(self, vals):
        if vals.get('tour_number', 'New') == 'New':
            vals['tour_number'] = self.env['ir.sequence'].next_by_code(
                'sale.order.template') or 'New'
        result = super(TravelPackage, self).create(vals)
        return result

    def create_itinerary_date(self, start_date, end_date):
        date_data_list = []
        if isinstance(start_date, str):
            start_date = datetime.strptime(
                start_date, DEFAULT_SERVER_DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, DEFAULT_SERVER_DATE_FORMAT)
        i = 0
        while start_date <= end_date:
            i = i + 1
            vals = {'itinerary_date': start_date,
                    'description': 'Day' + str(i)}
            date_data_list.append((0, 0, vals))
            start_date = start_date + relativedelta(days=+1)
        return date_data_list

    def action_generate_itinerary_plan(self):
        if self.arrival_date and self.return_date:
            self.itinerary_ids = [(5,)]
            self.itinerary_ids = self.create_itinerary_date(
                self.arrival_date, self.return_date)

    def action_fetch_cost_sale_price(self):
        for rec in self.group_costing_ids:
            rec.cost_price = (rec.number_of_adult + rec.number_of_children) * \
                rec.sale_order_template_id.cost_per_person
            rec.sales_price = (rec.number_of_adult + rec.number_of_children) * \
                rec.sale_order_template_id.sell_per_person

    @api.constrains('arrival_date', 'return_date')
    def check_arrival_return_date(self):
        current_date = fields.Date.context_today(self)
        for package in self:
            if package.arrival_date and package.return_date:
                if package.arrival_date < current_date:
                    raise ValidationError(
                        _('''Arrival date should be greater than the current date.'''))
                if package.arrival_date > package.return_date:
                    raise ValidationError(
                        _('''Return date should be greater than arrival date.'''))

    @api.constrains('state')
    def check_itinerary_ids(self):
        for rec in self:
            if not rec.itinerary_ids and rec.state == 'confirm':
                raise ValidationError(
                    _('''Please add itinerary lines before confirm the package '%s'.''' % (rec.name,)))

    @api.constrains('pax_group', 'max_pax_group')
    def _check_travellers_number(self):
        for package in self:
            if package.max_pax_group == 0 or package.pax_group == 0:
                raise UserError(
                    _('''Number of maximum/minimum travellers should be '''
                      '''greater than zero'''))
            elif package.pax_group >= package.max_pax_group:
                raise UserError(
                    _('''Number of maximum travellers should be '''
                        '''greater than minimum number of travellers'''))

    def compute_total_passenger(self):
        self.total_passenger = 0.0
        for package in self:
            orders = self.env['sale.order'].search(
                [('sale_order_template_id', '=', package.id),
                 ('state', '=', 'sale')])
            count = sum(len(order.passenger_ids) for order in orders)
            package.total_passenger = count

    def button_passenger_total(self):
        for package in self:
            confirm_reg = self.env['sale.order'].search(
                [('sale_order_template_id', '=', package.id),
                 ('state', '=', 'sale')])
            passenger = self.env['travellers.list'].search(
                [('sale_order_id', 'in', confirm_reg.ids)])
        return {
            'name': "Passenger List",
            'views': [(
                self.env.ref('tour_travel_management.passenger_list_tree').
                    id, 'tree'),
                (self.env.ref('tour_travel_management.passenger_list_form'
                              ).id, 'form')],
            'view_mode': 'tree',
            'res_model': 'travellers.list',
            'res_id': passenger and passenger.ids,
            'type': 'ir.actions.act_window',
            'domain': [('sale_order_id', 'in', confirm_reg.ids)],
            'target': 'current',
            'context': {'create': False},
        }

    def button_registration_total(self):
        for package in self:
            confirm_reg = self.env['sale.order'].search(
                [('sale_order_template_id', '=', package.id)])
        return {
            'name': "Registration List",
            'views': [(
                self.env.ref('sale.view_quotation_tree_with_onboarding').
                    id, 'tree'), (self.env.ref(
                        'tour_travel_management.tour_package_registration_form'
                    ).id, 'form')],
            'view_mode': 'tree',
            'res_model': 'sale.order',
            'res_id': confirm_reg and confirm_reg.ids,
            'type': 'ir.actions.act_window',
            'domain': [('sale_order_template_id', '=', package.id)],
            'target': 'current',
            'context': {'create': False},
        }

    def button_confirm(self):
        self.write({"state": "confirm"})

    def button_done(self):
        self.write({"state": "done"})

    def button_draft(self):
        self.write(
            {'state': 'draft',
             'sale_order_template_line_ids': [(5, 0,)]})

    def button_cancel(self):
        self.write({"state": "cancel"})

    def create_rfq(self):
        view = self.env.ref(
            'purchase.purchase_order_form')
        return {
            'name': _('Generate RFQ'),
            'type': 'ir.actions.act_window',
            'binding_view_types': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': self.env.context,
        }

    def open_rfq_view(self):
        purchase_orders = self.env['purchase.order'].search(
            [('package_id', 'in', [self.id])])
        action = self.env.ref(
            'purchase.purchase_rfq').read()[0]
        if len(purchase_orders) > 1:
            action['domain'] = [('id', 'in', purchase_orders.ids)]
        elif len(purchase_orders) == 1:
            action['views'] = \
                [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_orders.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class PackageCategory(models.Model):
    _name = "package.category"
    _description = "Package Category Type"

    def _compute_package_count(self):
        for rec in self:
            rec.package_count = self.env['sale.order.template'].search_count(
                [('category_id', '=', rec.id), ('active', '=', True)])

    name = fields.Char(string="Category", required=True)
    todo_package = fields.Integer(
        string='TODO',
        compute='_compute_state_package',
    )
    in_draft = fields.Integer(
        'Draft',
        compute='_compute_state_package')
    in_confirm = fields.Integer(
        'Confirmed',
        compute='_compute_state_package')
    in_done = fields.Integer(
        'Done',
        compute='_compute_state_package')
    in_cancel = fields.Integer(
        'Cancelled',
        compute='_compute_state_package')
    sale_order_template_ids = fields.One2many(
        'sale.order.template',
        'category_id',
        'Sale Order Template')
    package_count = fields.Integer(
        "Package Count", compute="_compute_package_count")

    @api.depends('sale_order_template_ids.state')
    def _compute_state_package(self):
        """Compute number of packages in
        different state"""
        for category in self:
            category.todo_package = len(
                category.sale_order_template_ids.filtered(
                    lambda package: package.state in ['draft', 'confirm'] and package.active == True))
            category.in_draft = len(
                category.sale_order_template_ids.filtered(
                    lambda package: package.state == 'draft' and package.active == True))
            category.in_done = len(
                category.sale_order_template_ids.filtered(
                    lambda package: package.state == 'done' and package.active == True))
            category.in_cancel = len(
                category.sale_order_template_ids.filtered(
                    lambda package: package.state == 'cancel' and package.active == True))
            category.in_confirm = len(
                category.sale_order_template_ids.filtered(
                    lambda package: package.state == 'confirm' and package.active == True))
