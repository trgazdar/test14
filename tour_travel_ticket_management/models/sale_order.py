#  See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrderTemplete(models.Model):
    _inherit = "sale.order.template"

    ticket_package_line_ids = fields.One2many('ticket.package.line',
                                             'sale_order_templete_id', 
                                             string='Ticket Package Lines')
    visa_package_line_ids = fields.One2many('visa.package.line',
                                             'sale_order_templete_id', 
                                             string='Visa Package Lines')

    def get_cost_price(self):
        res = super(SaleOrderTemplete, self).get_cost_price()
        for order in self:
            visa_price = sum(
                [line.cost_price for line in order.visa_package_line_ids])
            ticket_price = sum(
                [line.cost_price * line.qty for line in order.ticket_package_line_ids if line.qty != 0])
        return res + visa_price + ticket_price

    def get_sell_price(self):
        res = super(SaleOrderTemplete, self).get_sell_price()
        for order in self:
            visa_sell_price = sum(
                [line.unit_price for line in order.visa_package_line_ids])
            ticket_sell_price = sum(
                [line.unit_price * line.qty for line in order.ticket_package_line_ids if line.qty != 0])
        return res + visa_sell_price + ticket_sell_price

    # Develogers Start
    def _generate_purchase_order_vals(self):
        vals = super(SaleOrderTemplete,self)._generate_purchase_order_vals()
        ticket_line_ids = self.ticket_package_line_ids
        supplier_ids = ticket_line_ids.supplier_id
        for supplier in supplier_ids:
            ticket_packages = []
            for line in ticket_line_ids:
                if line.supplier_id.id == supplier.id:
                    ticket_packages.append((0,0,{
                        'product_id': line.product_id.id,
                        'product_qty': line.qty,
                        'price_unit': line.product_id.standard_price,
                    }))
            purchase_order = {
                'partner_id': supplier.id,
                'order_line': ticket_packages,
                'package_id' : self.id,
            }
            vals.append(purchase_order)       
        return vals

    """
    @api.onchange('ticket_package_line_ids','ticket_package_line_ids.qty','ticket_package_line_ids.cost_price')
    def get_amount_total_without_commission(self):
        print("Ticket")
        _logger.info("ticket")
        super(SaleOrderTemplete,self).get_amount_total_without_commission()
    """
    # Devenders End
    
    @api.depends('ticket_package_line_ids.cost_price', 'visa_package_line_ids.cost_price')
    def _compute_cost_per_person(self):
        for order in self:
            total_cost = self.get_cost_price()
            order.update({'cost_per_person': total_cost})

    @api.depends('ticket_package_line_ids.unit_price', 'visa_package_line_ids.unit_price')
    def _compute_sell_per_person(self):
        for order in self:
            total_sale_price = self.get_sell_price()
            order.update({'sell_per_person': total_sale_price})


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    ticket_line_ids = fields.One2many('tour.registration.line', 'ticket_sale_id', 'Tickets')

    def get_package_ticket_lines(self):
        package_lines = []
        template = self.sale_order_template_id.with_context(
            lang=self.partner_id.lang)
        for line in template.ticket_package_line_ids:
            data = {'name': line.display_name,
                    'display_type': line.display_type}
            pax_qty = 1
            total_pax = (self.adults + self.children)
            if total_pax > 1:
                pax_qty = total_pax
            qty = 1
            while qty <= pax_qty:
                if not line.display_type:
                    data = {
                        'name':line.product_id.display_name,
                        'ticket_product_id': line.product_id.id,
                        'source_id': line.source_id.id,
                        'destination_id': line.destination_id.id,
                        'fare_type_id': line.fare_type_id.id,
                        'display_type': line.display_type,
                        'price_unit': line.unit_price,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_id.uom_id.id,
                        'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                    }
                    qty += 1
                package_lines.append((0, 0, data))
        return package_lines

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        order_lines = self.get_package_ticket_lines()
        self.ticket_line_ids = [(5,)]
        self.update({'ticket_line_ids': order_lines})
        for rec in self.ticket_line_ids:
            if rec.display_type == False:
                rec.onchange_ticket_qty()
                rec._compute_tax_id()
        return super(SaleOrder, self).onchange_sale_order_template_id()


class TourRegistrationLine(models.Model):
    _inherit = 'tour.registration.line'

    ticket_sale_id = fields.Many2one('sale.order','Ticket Order',ondelete='cascade')
    ticket_product_id = fields.Many2one('product.product','Ticket')
    source_id = fields.Many2one('city.city', 'Source')
    destination_id = fields.Many2one('city.city', 'Destination')
    passenger_id = fields.Many2one('travellers.list', 'Passenger', ondelete='restrict')
    issue_date = fields.Date('Issue Date')
    fare_type_id = fields.Many2one("fare.type", "Fare Type",
                                   ondelete='restrict')
    ticket_no = fields.Char("Ticket No")

    @api.model
    def create(self, vals):
        if 'ticket_sale_id' in vals:
            sale = self.env["sale.order"].browse(vals['ticket_sale_id'])
            vals.update({'order_id': sale.id})
        return super(TourRegistrationLine, self).create(vals)

    def set_ticket_description(self):
        name_list = []
        if self.passenger_id.name:
            name_list.append("Passenger:  %s" % (self.passenger_id.name))
        if self.ticket_product_id and self.fare_type_id:
            name_list.append("%s, %s" % (self.fare_type_id.name, self.ticket_product_id.name))
        if self.source_id and self.destination_id:
            name_list.append("%s -> %s" % (self.source_id.name, self.destination_id.name))
        if self.ticket_no:
            name_list.append("PNR No: %s" % (self.ticket_no))
        name = '\n'.join(name_list)
        return name

    @api.onchange('fare_type_id', 'passenger_id', 'source_id', 'destination_id', 'ticket_no')
    def onchange_ticket_qty(self):
        for rec in self:
            rec.name = rec.set_ticket_description() or rec.name

    @api.onchange('ticket_product_id')
    def onchange_ticket_product_id(self):
        if self.ticket_product_id:
            self.update({'product_id': self.ticket_product_id.id,
                         'order_id': self.ticket_sale_id.id})
            self.product_id_change()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ticket_id = fields.Many2one('ticket.package.line','Ticket')
    visa_id = fields.Many2one('visa.package.line','Visa')
