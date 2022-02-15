from odoo import fields, models, api


class ControlGuias(models.Model):
    _name = "control_guias"
    _description = "Control de guias"

    fecha_envio = fields.Date("Fecha de envio")
    fecha_entrega = fields.Date("Fecha de entrega")
    cliente_id = fields.Many2one("res.partner", "Cliente")
    destino = fields.Char("Destino")
    marca = fields.Char("Marca")
    modelo = fields.Char("Modelo")
    color = fields.Char("Color")
    destinatario_id = fields.Many2one("res.partner", "Destinatario")
    cod_ciguena = fields.Char("Cod.Ciguena")
    remitente = fields.Char("G.Rem.Remitente")
    num_chasis = fields.Char("Numero de chasis")
    pikango = fields.Char("G.R.T Pikango")
    servintes = fields.Char("G.R.T Servintes")
    cliente_final_id = fields.Many2one("res.partner", "Cliente Final")
    monto_guia = fields.Float("Monto Guia")
    impuesto = fields.Float("Impuesto")
    precio = fields.Float("Precio")
    valor = fields.Float("Valor")
    estado = fields.Selection(selection=[("pagado", "Pagado"), ("nopagado", "NoPagado")], string="Estado de Pago",
                              default="pagado", required=True)

    @api.onchange('monto_guia', 'impuesto', 'precio')
    def _onchange_precio(self):
        self.precio = self.monto_guia + self.impuesto