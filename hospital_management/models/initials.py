from odoo import api, fields, models


class Initials(models.Model):
    _name="name.initials"
    _description="Initials"

    name = fields.Char(string="Initials", required=True)