from odoo import api, fields, models


class WithholdingTable(models.Model):
    _name = 'withholding.tax.table'
    _description = 'Tabla de Retenciones'

    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    percent = fields.Float(string='Porcentaje')

    def name_get(self):
        res = []
        for record in self:
            complete_name = f"{record.code}: {record.name}"
            res.append((record.id, complete_name))
        return res