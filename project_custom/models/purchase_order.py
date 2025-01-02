from odoo import fields , models, api
from odoo.http import request
from odoo.exceptions import ValidationError
import logging

_logger  = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_state = fields.Selection([('draft','Draft'),('first_approval' , 'First Approval'),('second_approval','Second Approval')], default='draft', string="User Approval State", readonly=True)

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        # NOTE : what credit i have will be compared by global value stored in settings:
        i_have = self.partner_id.credit_limit
        icp = request.env['ir.config_parameter'].sudo()
        global_credit = float(icp.get_param('res.config.global_credit_limit'))
        if i_have > global_credit:
            self.write({'approval_state': 'first_approval'})
            print('I Have ', i_have)
        else:
            _logger.info('Your Credit Limit is lesser then global credit')
        return True