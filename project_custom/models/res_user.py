from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Becouse there is no more name_get method is used in odoo 17
    def _compute_display_name(self):
        for user in self:
            user.display_name = f'{user.name} / {user.login}'
