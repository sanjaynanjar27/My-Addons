    # -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import models, fields


class LogoutAllDevicesWizard(models.TransientModel):
    _name = 'logout.all.devices.wizard'
    _description = 'Logout from All Devices Confirmation'

    def action_confirm_logout(self):
        # Perform the logout logic
        user_id = self.env.context.get('active_id')
        user = self.env['res.users'].browse(user_id)
        return {'type': 'ir.actions.act_url', 'url': '/logg_out_from_all_device', 'target': 'self', }
