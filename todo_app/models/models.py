# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class todo_app(models.Model):
#     _name = 'todo_app.todo_app'
#     _description = 'todo_app.todo_app'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

#Clases que se requieren
from odoo import models,fields

class ToDo(models.Model):
    _name="todo.app"
    _description="Lista de tareas"
    _rec_name="name"
    #El atributo name, el nombre es variable reservada
    name=fields.Char(String="Nombre")
    state=fields.Char(String="Estado")
    description=fields.Char(string="Descripcion")
    #title=fields.Char(String="Titulo")
    #price=fields.Float(varchar="Precio")


