from odoo import fields, api, models


class ToDoItem(models.Model):
    _name = "todo.item"
    _description = 'To do item..'

    items = fields.Char(string="Single item")
    list_id = fields.Many2one('todo.list', string="List")


class ToDoListData(models.Model):
    _name = "todo.list"
    _description = 'To do list..'

    name = fields.Char(string="List Heading")
    items = fields.One2many('todo.item', 'list_id', string="Items")
    user_id = fields.Many2one('res.users', string="User")
    date_created = fields.Datetime(string="Date Created")
