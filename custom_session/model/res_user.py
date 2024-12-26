    # -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import fields, models, api
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class Users(models.Model):
    _inherit = ["res.users"]
    session_count = fields.Integer(string="Session Time Out",default=604800,copy=False)


    def action_logout_all_devices(self):
        """Logs out the user from all devices by revoking their sessions."""
        user = request.session.uid
        print(user)
        user_login_history = request.env['res.users.logger'].search([('session_id', '!=', False)])
        current_session = request.session.sid  # Current logged-in user
        print("Current Session",current_session)
        for record in user_login_history:
            if record.username.id == user:
                request.session.sid = record.session_id
                request.session.logout()
                print("History : ",record.username)
