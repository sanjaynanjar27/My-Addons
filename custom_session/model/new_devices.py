    # -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
import logging
from odoo import models, fields, api, tools
from odoo.http import root, request, Session, Application, FilesystemSessionStore, FutureResponse, GeoIP

_logger = logging.getLogger(__name__)


class UserLoginHistory(models.Model):
    _name = 'user.login.history'
    _description = 'User Login History'

    user_id = fields.Many2one('res.users', string='User', required=True)
    ip_address = fields.Char('IP Address')
    login_time = fields.Datetime('Login Time')
    logout_time = fields.Datetime('Logout Time')
    device_type = fields.Selection(
        [('desktop', 'Desktop'), ('mobile', 'Mobile')],
        string='Device Type',
        default='desktop'
    )
    browser = fields.Char('Browser')
    mobile = fields.Boolean('Is Mobile', default=False)
    session_id = fields.Char('Session ID')  # Store session ID
    revoked = fields.Boolean("Revoked",
                             help="""If True, the session file corresponding to this device
                                        no longer exists on the filesystem.""")

    @api.model
    def update_logout_time(self):
        """ This method can be used to update the logout time when session ends """
        # Find all the active login records for the current session and update logout time
        history_records = self.search([('session_id', '=', request.session.sid)])
        for record in history_records:
            record.logout_time = fields.Datetime.now()

    def find_session(self):
        session_info = request.env['ir.http'].session_info()
        print(session_info)

    def action_delete_session(self):
        print('action_delete_session')


class UserLoginPasswordConfirm(models.TransientModel):
    _name = 'user.login.password.confirm'
    _description = 'Password Confirmation'

    password = fields.Char(string="Password")

    def confirm_password(self):
        print("Working", self.env.context.get('active_id'))


root.rotate = FilesystemSessionStore().rotate
