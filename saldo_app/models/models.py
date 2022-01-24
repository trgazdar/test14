from email.policy import default
from odoo import fields, models

class Movimiento(models.Model):
    _name="sa.movimiento" #sa_movimiento
    _description = "Movimiento"
    _inherit="mail.thread"
    
    #El ID odoo lo maneja solo
    name=fields.Char("Nombre")
    #Hay 2, uno para almacenarse y otro para mostrarse
    type_move=fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")],string="Tipo", default="ingreso", required=True)
    date=fields.Datetime("Fecha")
    amount=fields.Float("Monto", track_visibility="onchange")
    receipt_image=fields.Binary("Foto del recibo")
    notas=fields.Html("Notas")
    currency_id=fields.Many2one("res.currency", default=162)
    

    #El Many2one puede existir sin el One2many, pero no al reves
    user_id=fields.Many2one("res.users",string="Usuario", default=lambda self: self.env.user.id)
    category_id=fields.Many2one("sa.category","Categoria")
    
    #puedo perzonalizar la tabla q creara odoo y los campos
    tag_ids=fields.Many2many("sa.tag","sa_mov_sa_tag_rel","move_id","tag_id") #Odoo creara: sa_movimiento_sa_tag_rel
    
class Category(models.Model):
    _name="sa.category"
    _description="Categoria"
    
    name=fields.Char("Nombre")
    
    def ver_movimientos(self):
        return {
            "type":"ir.actions.act_window",
            "name":"Movimientos de Categoria :" + self.name,
            "res_model":"sa.movimiento",
            "views":[[False,"tree"]],
            "target":"self",
            "domain":[["category_id","=",self.id]]
        }

class Tag(models.Model):
    _name="sa.tag"
    _description="Tag"
    
    name=fields.Char("Nombre")
    
#el nombre puede ser cualquier, solo haremos referencia a una 
# #tabla existente
#extendemos un modleo
#El one2many, necesita que haya antes un Many2one en el otro modelo
class ResUsers(models.Model):
    _inherit="res.users"
    
    #Le doy el modelo(tabla) y campo al que hara referencia
    movimiento_ids=fields.One2many("sa.movimiento","user_id")
    
