from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    vat = fields.Char(string='DNI')