from odoo import models, api
from odoo.exceptions import ValidationError

class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, values):
        return super(MailMail, self).create(values)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def message_post(self, **kwargs):
        if 'partner_ids' in kwargs:
            partners = self.env['res.partner'].browse(kwargs['partner_ids'])
            kwargs['partner_ids'] = partners.filtered(lambda p: not p.restrict_mail).ids
            print(f"Filtered Partners: {partners}")
        return super(MailThread, self).message_post(**kwargs)
