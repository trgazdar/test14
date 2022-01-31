from odoo import fields, models, api


class ControlGuias(models.Model):
    _name="control_guias"
    _description="Control de guias"

    fecha_envio=fields.Date("Fecha de envio")
    fecha_entrega=fields.Date("Fecha de entrega")
    cliente_id=fields.Many2one("res.partner","Cliente")
    destino=fields.Char("Destino")
    marca=fields.Char("Marca")
    modelo=fields.Char("Modelo")
    color=fields.Char("Color")
    destinatario_id=fields.Many2one("res.partner","Destinatario")
    cod_ciguena=fields.Char("Cod.Ciguena")
    remitente=fields.Char("G.Rem.Remitente")
    num_chasis=fields.Char("Numero de chasis")
    pikango=fields.Char("G.R.T Pikango")
    servintes=fields.Char("G.R.T Servintes")
    cliente_final_id=fields.Many2one("res.partner","Cliente Final")
    valor=fields.Float("Valor")
    estado=fields.Selection(selection=[("pagado","Pagado"),("nopagado","NoPagado")],string="Estado de Pago",
    default="pagado",required=True)


class Facturacion(models.Model):
    _inherit="account.move"
    
    fecha_inicial=fields.Date("Fecha inicial")
    fecha_final=fields.Date("Fecha final")
    guias_control_ids=fields.Many2many("control_guias","Guias")

    @api.onchange('fecha_incial','fecha_final','partner_id')
    def _onchange_guias_control_ids(self):

        if self.partner_id and self.fecha_final and self.fecha_inicial:

            busqueda_guia=self.env['control_guias'].search(
                [('cliente_id','=',self.partner_id.id)]
            )

            self.guias_control_ids=busqueda_guia







