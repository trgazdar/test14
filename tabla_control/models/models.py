from odoo import fields, models


class ControlGuias(models.Model):
    _name="control_guias"
    _description="Control de guias"

    fecha_envio=fields.Datetime("Fecha de envio")
    fecha_entrega=fields.Datetime("Fecha de entrega")
    cliente=fields.Char("Cliente")
    destino=fields.Char("Destino")
    marca=fields.Char("Marca")
    modelo=fields.Char("Modelo")
    color=fields.Char("Color")
    destinatario=fields.Char("Destinatario")
    cod_ciguena=fields.Char("Cod.Ciguena")
    remitente=fields.Char("G.Rem.Remitente")
    num_chasis=fields.Integer("Numero de chasis")
    pikango=fields.Char("G.R.T Pikango")
    servintes=fields.Char("G.R.T Servintes")
    cliente_final=fields.Char("Cliente Final")
    valor=fields.Float("Valor")
    estado=fields.Selection(selection=[("pagado","Pagado"),("no pagado","No Pagado")],string="Estado de Pago",
    default="pagado",required=True)


class Facturacion(models.Model):
    _name="facturacion"
    _description="Facturacion"

    name=fields.Char("Nombre")

