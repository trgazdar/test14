from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
    #Nombre del modelo al que debo relacionar, muchos movimientos son de 1 usuario
    user_id=fields.Many2one("res.users",string="Usuario", default=lambda self: self.env.user.id)
    category_id=fields.Many2one("sa.category","Categoria")
    email=fields.Char(related="user_id.email",string="Correo electronico")

    #puedo perzonalizar la tabla q creara odoo y los campos
    tag_ids=fields.Many2many("sa.tag","sa_mov_sa_tag_rel","move_id","tag_id") #Odoo creara: sa_movimiento_sa_tag_rel
    
    
    @api.constrains("amount")
    def _check_amount(self):
        if not(self.amount>=0 and self.amount<=100000):
            raise ValidationError("El monto debe encontrarse entre 0 y 100,000")

    @api.onchange("type_move")
    def onchange_type_move(self):
        if self.type_move=="ingreso":
            self.name = "Ingreso: "
        elif self.type_move=="gasto":
            self.name = "Gasto: "

    @api.model
    def create(self,vals):
        name=vals.get("name","-")
        amount=vals.get("amount","0")
        type_move=vals.get("type_move","")
        date=vals.get("date","")

        notas="""<p>Tipo de Movimiento: {}</p><p>Nombre: {}</p><p>Monto: {}</p><p>Fecha: {}</p>"""
        vals["notas"]=notas.format(type_move,name,amount,date)
        
        res=super(Movimiento,self).create(vals)
        return res

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
#tabla existente
#extendemos un modleo
#El one2many, necesita que haya antes un Many2one en el otro modelo
class ResUsers(models.Model):
    _inherit="res.users"
    
    #Le doy el modelo(tabla) y campo al que hara referencia
    movimiento_ids=fields.One2many("sa.movimiento","user_id")
    total_ingresos=fields.Float("Total de Ingresos", compute="_compute_movimientos")
    total_egresos=fields.Float("Total de Egresos", compute="_compute_")
    
    @api.depends("movimiento_ids")
    def _compute_movimientos(self):
        for record in self:
            record.total_ingresos= sum(record.movimiento_ids.filtered(lambda r:r.type_move=='ingreso').mapped("amount"))
            record.total_egresos= sum(record.movimiento_ids.filtered(lambda r:r.type_move=='gasto').mapped("amount"))

    
    def mi_cuenta(self):
        return {
            "type":"ir.actions.act_window",
            "name":"Mi cuenta",
            "res_model":"res.users",
            "res_id":self.env.user.id,
            "target":"self",
            "views":[(False,"form")]

        }