# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, api
from odoo.fields import Datetime
from odoo.http import request

from odoo.odoo.tools import default_parser


class UserLoginStatus(models.Model):
    _inherit = 'res.users'

    status = fields.Selection(selection=[
        ('done', 'Online'),
        ('blocked', 'Offline'),
    ], string="Login Status", default='blocked', readonly=True)
    total_log_record = fields.Integer('Total Log Information',compute='_count_total_log')
    is_session_expire = fields.Boolean('Is Session Expiry ?',default=False)
    session_expire_limit = fields.Integer('Expiry Timeout',default=0)

    def _count_total_log(self):
        for record in self:
            record.total_log_record = self.env['res.users.logger'].sudo().search_count([('username','=',record.id)])

    def show_log_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.users.logger",
            "domain": [('username','=',self.id)],
            "name": "User Logging Record",
            'view_mode': 'list',
        }

class UserLog(models.Model):
    _name = 'res.users.logger'
    _description = 'User Login/Logout Logger'

    username = fields.Many2one('res.users',"User Name")
    login_time = fields.Datetime("Login Time")
    logout_time = fields.Datetime("Logout Time")
    system_use_time = fields.Char("System Use Time",compute='_compute_system_use_time')
    session_id = fields.Char('Session')

    @api.model
    def save_session(self):
        user = self.env['res.users'].sudo().browse([request.uid])
        session = False
        if user:
            user.status = 'done'
            ICPSudo = self.env['ir.config_parameter'].sudo()
            need_to_store = ICPSudo.get_param('user_login_status.store_user_time')
            print("From Cit : ", request.session.sid)
            if need_to_store:
                session = self.sudo().create({
                    'username': request.uid,
                    'login_time': Datetime.now(),
                    'session_id': request.session.sid
                })
        try:
            self.env.cr.commit()
        except:
            pass
        return session

    def _on_logout(self):
        self.username.status = 'blocked'
        self.sudo().write(
            {
                'logout_time': Datetime.now(),
                'session_id': False
            }
        )
        self._cr.commit()

    def _compute_system_use_time(self):
        for record in self:
            if record.logout_time:
                time_diff = str(record.logout_time - record.login_time)
            else:
                time_diff = str(fields.Datetime.now() - record.login_time)
            time_diff = time_diff[:time_diff.find('.')]
            record.system_use_time = time_diff
