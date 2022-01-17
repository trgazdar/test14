# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo import tools
from odoo.exceptions import UserError, ValidationError,Warning


class fleet_repair(models.Model):
    _name = 'fleet.repair'
    _inherit = ['mail.thread']
    name = fields.Char(string='Subject', required=True)
    sequence = fields.Char(string='Sequence', readonly=True ,copy =False)
    client_id = fields.Many2one('res.partner', string='Client', required=True)
    client_phone = fields.Char(string='Phone')
    client_mobile = fields.Char(string='Mobile')
    client_email = fields.Char(string='Email')
    receipt_date = fields.Date(string='Date of Receipt')
    contact_name = fields.Char(string='Contact Name')
    phone = fields.Char(string='Contact Number')
    fleet_id = fields.Many2one('fleet.vehicle','Fleet')
    license_plate = fields.Char('License Plate', help='License plate number of the vehicle (ie: plate number for a car)')
    vin_sn = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)')
    model_id = fields.Many2one('fleet.vehicle.model', 'Model', help='Model of the vehicle')
    fuel_type = fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle')
    guarantee = fields.Selection(
              [('yes', 'Yes'), ('no', 'No')], string='Under Guarantee?')
    guarantee_type = fields.Selection(
            [('paid', 'paid'), ('free', 'Free')], string='Guarantee Type')
    service_type = fields.Many2one('service.type', string='Nature of Service')
    user_id = fields.Many2one('res.users', string='Assigned to')
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
    description = fields.Text(string='Notes')
    service_detail = fields.Text(string='Service Details')
    state = fields.Selection([
            ('draft', 'Received'),
            ('diagnosis', 'In Diagnosis'),
            ('diagnosis_complete', 'Diagnosis Complete'),
            ('quote', 'Quotation Sent'),
            ('saleorder', 'Quotation Approved'),
            ('workorder', 'Work in Progress'),
            ('work_completed', 'Work Completed'),
            ('invoiced', 'Invoiced'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
            ], 'Status', default = "draft",readonly=True, copy=False, help="Gives the status of the fleet repairing.", select=True)
    diagnose_id = fields.Many2one('fleet.diagnose', string='fleet Diagnose', copy=False)
    workorder_id = fields.Many2one('fleet.workorder', string='fleet Work Order', copy=False)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', copy=False)
    fleet_repair_line = fields.One2many('fleet.repair.line', 'fleet_repair_id', string="fleet Lines")
    workorder_count = fields.Integer(string='Work Orders', compute='_compute_workorder_id')
    dig_count  = fields.Integer(string='Diagnosis Orders', compute='_compute_dignosis_id')
    quotation_count = fields.Integer(string ="Quotations", compute='_compute_quotation_id')
    saleorder_count = fields.Integer(string = "Sale Order", compute='_compute_saleorder_id')
    confirm_sale_order = fields.Boolean('is confirm')  

    
    _order = 'id desc'

    def button_view_diagnosis(self):
        list = []
        context = dict(self._context or {})
        dig_order_ids = self.env['fleet.diagnose'].search([('fleet_repair_id', '=', self.id)])           
        for order in dig_order_ids:
            list.append(order.id)
        return {
            'name': _('Fleet Diagnosis'),
            'binding_view_types': 'form',
            'view_mode': 'tree,form',
            'res_model': 'fleet.diagnose',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in',list )],
            'context': context,
        }


    def button_view_workorder(self):
        list = []
        context = dict(self._context or {})
        work_order_ids = self.env['fleet.workorder'].search([('fleet_repair_id', '=', self.id)])           
        for order in work_order_ids:
            list.append(order.id)
        return {
            'name': _('Fleet Work Order'),
            'binding_view_types': 'form',
            'view_mode': 'tree,form',
            'res_model': 'fleet.workorder',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in',list )],
            'context': context,
        }


    def button_view_workorder(self):
        list = []
        context = dict(self._context or {})
        work_order_ids = self.env['fleet.workorder'].search([('fleet_repair_id', '=', self.id)])           
        for order in work_order_ids:
            list.append(order.id)
        return {
            'name': _('Fleet Work Order'),
            'binding_view_types': 'form',
            'view_mode': 'tree,form',
            'res_model': 'fleet.workorder',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in',list )],
            'context': context,
        }
  
  

    def button_view_quotation(self):
        list = []
        context = dict(self._context or {})
        quo_order_ids = self.env['sale.order'].search([('state', '=', 'draft'),('fleet_repair_id', '=', self.id)])           
        for order in quo_order_ids:
            list.append(order.id)
        return {
            'name': _('Sale'),
            'binding_view_types': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in',list )],
            'context': context,
        }
  
    def button_view_saleorder(self):
        list = []
        context = dict(self._context or {})
        quo_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', self.id)])           
        for order in quo_order_ids:
            list.append(order.id)
        return {
            'name': _('Sale'),
            'binding_view_types': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in',list )],
            'context': context,
        }
 
    def button_view_invoice(self):
        list = []
        inv_list  = []
        so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', self.id)])
        for order in so_order_ids:
            inv_order_ids = self.env['account.move'].search([('invoice_origin', '=',order.name )])            
            if inv_order_ids:
                for order_id in inv_order_ids:
                    if order_id.id not in list:
                        list.append(order_id.id)
                            

        context = dict(self._context or {})
        return {
            'name': _('Invoice '),
            'binding_view_types': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in',list )],
            'context': context,
        }
 
  
    
    @api.depends('workorder_id')
    def _compute_workorder_id(self):
        for order in self:
            work_order_ids = self.env['fleet.workorder'].search([('fleet_repair_id', '=', order.id)])            
            order.workorder_count = len(work_order_ids)


    @api.depends('diagnose_id')
    def _compute_dignosis_id(self):
        for order in self:
            dig_order_ids = self.env['fleet.diagnose'].search([('fleet_repair_id', '=', order.id)])            
            order.dig_count = len(dig_order_ids)


    @api.depends('sale_order_id')
    def _compute_quotation_id(self):
        for order in self:
            quo_order_ids = self.env['sale.order'].search([('state', '=', 'draft'),('fleet_repair_id', '=', order.id)])            
            order.quotation_count = len(quo_order_ids)
    
    @api.depends('confirm_sale_order')
    def _compute_saleorder_id(self):
        for order in self:
            order.quotation_count = 0
            so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', order.id)])            
            order.saleorder_count = len(so_order_ids)
          

    @api.model
    def default_get(self,fields):
        res = super(fleet_repair, self).default_get(fields)
        res['sequence'] = self.env['ir.sequence'].get('fleet.repair')
        return res


    def diagnosis_created(self):
        self.write({'state':'diagnosis'})

    def quote_created(self):
        self.write({'state':'quote'})

    def order_confirm(self):
        self.write({'state':'saleorder'})

    def fleet_confirmed(self):
        self.write({'state':'confirm'})

    def workorder_created(self):
        self.write({'state':'workorder'})

    @api.onchange('client_id')
    def onchange_partner_id(self):
        addr = {}
        if self.client_id:
            addr = self.client_id.address_get(['contact'])
            addr['client_phone'] = self.client_id.phone
            addr['client_mobile'] = self.client_id.mobile
            addr['client_email'] = self.client_id.email
        return {'value': addr}


    def action_create_fleet_diagnosis(self):
        Diagnosis_obj = self.env['fleet.diagnose']
        fleet_line_obj = self.env['fleet.repair.line']
        repair_obj = self.env['fleet.repair'].browse(self._ids[0])
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        if not repair_obj.fleet_repair_line:
            raise Warning('You cannot create fleet Diagnosis without fleet.')
        
        diagnose_vals = {
            'service_rec_no': repair_obj.sequence,
            'name': repair_obj.name,
            'priority': repair_obj.priority,
            'receipt_date': repair_obj.receipt_date,
            'client_id': repair_obj.client_id.id,
            'contact_name': repair_obj.contact_name,
            'phone': repair_obj.phone,
            'client_phone': repair_obj.client_phone,
            'client_mobile': repair_obj.client_mobile,
            'client_email': repair_obj.client_email,
            'fleet_repair_id': repair_obj.id,
            'state': 'draft',
        }
        diagnose_id = Diagnosis_obj.create(diagnose_vals)
        for line in repair_obj.fleet_repair_line:
            fleet_line_vals = {
                'fleet_id': line.fleet_id.id,
                'license_plate': line.license_plate,
                'vin_sn': line.vin_sn,
                'fuel_type': line.fuel_type,
                'model_id': line.model_id.id,
                'service_type': line.service_type.id,
                'guarantee': line.guarantee,
                'guarantee_type':line.guarantee_type,
                'service_detail': line.service_detail,
                'diagnose_id': diagnose_id.id,
                'state': 'diagnosis',
                'source_line_id': line.id,
            }
            fleet_line_obj.create(fleet_line_vals)
            line.write({'state': 'diagnosis'})
        
        
        self.write({'state': 'diagnosis', 'diagnose_id': diagnose_id.id})
        result = mod_obj.get_object_reference('fleet_repair_management', 'action_fleet_diagnose_tree_view')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]
        res = mod_obj.get_object_reference('fleet_repair_management', 'view_fleet_diagnose_form')
        result['views'] = [(res and res[1] or False, 'form')]
        result['res_id'] = diagnose_id.id or False
        return result


    def action_print_receipt(self):
        assert len(self._ids) == 1, 'This option should only be used for a single id at a time'
        return self.env.ref('fleet_repair_management.fleet_repair_receipt_id').report_action(self)


    def action_print_label(self):
        if not self.fleet_repair_line:
            raise UserError(_('You cannot print report without fleet details'))

        assert len(self._ids) == 1, 'This option should only be used for a single id at a time'
        return self.env.ref('fleet_repair_management.fleet_repair_label_id').report_action(self)


    def action_view_quotation(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        order_id = self.sale_order_id.id
        result = mod_obj.get_object_reference('sale', 'action_orders')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]
        res = mod_obj.get_object_reference('sale', 'view_order_form')
        result['views'] = [(res and res[1] or False, 'form')]
        result['res_id'] = order_id or False
        return result

    
    def action_view_work_order(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        work_order_id = self.workorder_id.id
        result = mod_obj.get_object_reference('fleet_repair_management', 'action_fleet_workorder_tree_view')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]
        res = mod_obj.get_object_reference('fleet_repair_management', 'view_fleet_workorder_form')
        result['views'] = [(res and res[1] or False, 'form')]
        result['res_id'] = work_order_id or False
        return result


class service_type(models.Model):
    _name = 'service.type'
    
    name = fields.Char(string='Name')


class fleet_repair_line(models.Model):
    _name = 'fleet.repair.line'
    fleet_id = fields.Many2one('fleet.vehicle','Fleet')
    license_plate = fields.Char('License Plate', help='License plate number of the vehicle (ie: plate number for a car)')
    vin_sn= fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)')
    model_id= fields.Many2one('fleet.vehicle.model', 'Model', help='Model of the vehicle')
    fuel_type= fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle')
    guarantee= fields.Selection(
            [('yes', 'Yes'), ('no', 'No')], string='Under Guarantee?')
    guarantee_type= fields.Selection(
            [('paid', 'paid'), ('free', 'Free')], string='Guarantee Type')
    service_type= fields.Many2one('service.type', string='Nature of Service')
    fleet_repair_id= fields.Many2one('fleet.repair', string='fleet', copy=False)
    service_detail= fields.Text(string='Service Details')
    diagnostic_result= fields.Text(string='Diagnostic Result')
    diagnose_id= fields.Many2one('fleet.diagnose', string='fleet Diagnose', copy=False)
    workorder_id= fields.Many2one('fleet.workorder', string='fleet Work Order', copy=False)
    source_line_id= fields.Many2one('fleet.repair.line', string='Source')
    est_ser_hour= fields.Float(string='Estimated Sevice Hours')
    service_product_id= fields.Many2one('product.product', string='Service Product')
    service_product_price= fields.Float('Service Product Price')
    spare_part_ids= fields.One2many('spare.part.line', 'fleet_id', string='Spare Parts Needed')
    state= fields.Selection([
            ('draft', 'Draft'),
            ('diagnosis', 'In Diagnosis'),
            ('done', 'Done'),
            ], 'Status', default="draft", readonly=True, copy=False, help="Gives the status of the fleet Diagnosis.", select=True)

    _rec_name = 'fleet_id'


    def name_get(self):
        reads = self.read(['fleet_id', 'license_plate'])
        res = []
        for record in reads:
            name = record['license_plate']
            if record['fleet_id']:
                name = record['fleet_id'][1]
            res.append((record['id'], name))
        return res
        

    def action_add_fleet_diagnosis_result(self):
        for obj in self:
            self.write({'state': 'done'})
        return True
        
    @api.model
    def fields_view_get(self, view_id=None, binding_view_types='form', toolbar=False, submenu=False):
        res = super(fleet_repair_line,self).fields_view_get(view_id, binding_view_types, toolbar=toolbar, submenu=submenu)
        return res

    @api.onchange('fleet_id')
    def onchange_fleet_id(self):
        addr = {}
        if self.fleet_id:
            fleet = self.fleet_id
            addr['license_plate'] = fleet.license_plate
            addr['vin_sn'] = fleet.vin_sn
            addr['fuel_type'] = fleet.fuel_type
            addr['model_id'] = fleet.model_id.id
        return {'value': addr}


class fleet_repair_analysis(models.Model):
    _name = 'fleet.repair.analysis'

    id = fields.Integer('fleet Id', readonly=True)
    sequence =fields.Char(string='Sequence', readonly=True)
    receipt_date = fields.Date(string='Date of Receipt', readonly=True)
    state = fields.Selection([
            ('draft', 'Received'),
            ('diagnosis', 'In Diagnosis'),
            ('diagnosis_complete', 'Diagnosis Complete'),
            ('quote', 'Quotation Sent'),
            ('saleorder', 'Quotation Approved'),
            ('workorder', 'Work in Progress'),
            ('work_completed', 'Work Completed'),
            ('invoiced', 'Invoiced'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
            ], 'Status', readonly=True, copy=False, help="Gives the status of the fleet repairing.", select=True)
    client_id = fields.Many2one('res.partner', string='Client', readonly=True)
        

    _order = 'id desc'
