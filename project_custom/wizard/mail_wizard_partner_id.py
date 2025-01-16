from odoo import models, fields, api, _

class Invite(models.TransientModel):
    _inherit = 'mail.wizard.invite'

    partner_ids = fields.Many2many('res.partner', string='Recipients',domain=[('restrict_mail','=',False)])

