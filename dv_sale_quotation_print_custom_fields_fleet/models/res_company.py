from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    ## Header
    # Seccion 1
    header_first_section_title = fields.Char(string='Título de la primera sección')
    header_first_section_first_text = fields.Char(string='Texto primera línea')
    header_first_section_second_text = fields.Char(string='Texto segunda línea')
    
    # Seccion 2
    header_second_section_title = fields.Char(string='Título de la segunda sección')
    header_second_section_first_text = fields.Char(string='Texto primera línea')
    header_second_section_second_text = fields.Char(string='Texto segunda línea')
    
    # Seccion 3
    header_third_section_title = fields.Char(string='Título de la tercera sección')
    header_third_section_first_text = fields.Char(string='Texto primera línea')
    header_third_section_second_text = fields.Char(string='Texto segunda línea')
    
    ## Footer
    # Note
    footer_note = fields.Char(string='Nota de pie de página')
    # Seccion BBVA
    footer_first_section_first_text = fields.Char(string='Cuenta en Soles')
    footer_first_section_second_text = fields.Char(string='Cuenta en Dólares')
    
    # Seccion BCP
    footer_second_section_first_text = fields.Char(string='Cuenta en Soles')
    footer_second_section_second_text = fields.Char(string='Cuenta en Dólares')
    
    # Seccion INTERBANK
    footer_third_section_first_text = fields.Char(string='Cuenta en Soles')
    footer_third_section_second_text = fields.Char(string='Cuenta en Dólares')