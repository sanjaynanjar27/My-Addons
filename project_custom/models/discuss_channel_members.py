from odoo import api, models, fields


class DiscussChannelMembers(models.Model):
    _inherit = 'discuss.channel.member'

    partner_id = fields.Many2one("res.partner", "Partner", ondelete="cascade", index=True,
                                 domain=[('restrict_mail', '=', False)])
