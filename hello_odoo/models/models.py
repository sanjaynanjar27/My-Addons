from datetime import date

from odoo import models, fields, api


class Hello(models.Model):
    _name = 'hello.odoo'
    _inherit = 'product.product'

    name = fields.Char(name="Name")
    birth_date = fields.Date(string="Enter DAte")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    email = fields.Char(string="Email ID")
    age = fields.Char(string="Age",
                      compute="_compute_age_from_birthdate")  # # @api.depends('birth_date')  # def _compute_age_from_birthdate(self):  #  #  #

    @api.depends('birth_date')
    def _compute_age_from_birthdate(self):
        for rec in self:
            if rec.birth_date:
                birth_date = fields.Date.from_string(rec.birth_date)
                today = date.today()  # current date
                age = today.year - birth_date.year
                rec.age = age  # finding birthdate from selected date
            else:
                rec.age = 00
