from odoo import fields, models


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
    estado=fields.Selection(selection=[("pagado","Pagado"),("no_pagado","No Pagado")],string="Estado de Pago",
    default="pagado",required=True)


class Facturacion(models.Model):
    _name="facturacion"
    _description="Facturacion"

    name=fields.Char("Nombre")

