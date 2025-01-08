from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def message_post(self, **kwargs):
        # Check the followers
        followers = kwargs.get('partner_ids', [])
        restricted_partners = self.env['res.partner'].search([('restrict_mail', '=', True), ('id', 'in', followers)])
        print(restricted_partners)

        if restricted_partners:
            return self.env['mail.message'].create({
                'subject': _('Mail Restriction Applied'),
                'body': _('Emails will not be sent to restricted partners.'),
                'model': self._name,
                'res_id': self.id,
                'message_type': 'notification',
                'partner_ids': [(6, 0, followers)],
            })
        else:
            followers = list(set(followers) - set(restricted_partners.ids))
            kwargs['partner_ids'] = followers  # Remove restricted partners from recipients
            self.env['mail.message'].create({
                'subject': _('Mail Restriction Applied'),
                'body': _('Emails will not be sent to restricted partners.'),
                'model': self._name,
                'res_id': self.id,
                'message_type': 'notification',
                'partner_ids': [(6, 0, followers)],
            })
            return super(SaleOrder, self).message_post(**kwargs)
