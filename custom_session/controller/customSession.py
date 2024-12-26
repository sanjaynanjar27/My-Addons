    # -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import http
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.session import Session
from odoo.http import request
import re
import logging
_logger = logging.getLogger(__name__)


class IdleTimeController(http.Controller):
    @http.route('/get_idle_time/timer', type='json', auth='user')
    def get_idle_time(self):
        user = request.env.user
        return user.session_count or 0.10  # Default to 5 minutes if not set

class HomeInherit(Home):
    @http.route('/web/login', type='http', auth='public', methods=['POST'], csrf=True)
    def custom_login(self, redirect=None, **kw):
        # Call the original web_login function to maintain the normal login behavior
        res = super(HomeInherit, self).web_login(redirect=redirect, **kw)
        if 'login_success' in request.params and request.params['login_success']:

            user = request.env['res.users'].sudo().search([('login', '=', kw['login'])], limit=1)
            if user:
                session_id = request.session.sid
                ip_address = request.httprequest.remote_addr
                user_agent = str(request.httprequest.user_agent)
                device_type, browser, mobile = self._parse_user_agent(user_agent)
                user_data = request.env['user.login.history'].sudo().create(
                    {
                        'user_id': user.id,
                        'ip_address': ip_address,
                        'device_type': device_type,
                        'browser': browser,
                        'mobile': mobile,
                    }
                )
                return res
        return res

    def _parse_user_agent(self, user_agent):
        """
        Parse the User-Agent string to identify device type, browser, and mobile.
        """
        device_type = 'desktop'
        browser = 'unknown'
        mobile = False

        mobile_regex = re.compile(r"Mobile|Android|iPhone|iPad", re.IGNORECASE)
        browser_regex = re.compile(r"Chrome|Firefox|Safari|Edge|MSIE|Trident", re.IGNORECASE)

        if mobile_regex.search(user_agent):
            device_type = 'mobile'
            mobile = True

        browser_match = browser_regex.search(user_agent)
        if browser_match:
            browser = browser_match.group()

        return device_type, browser, mobile


class SessionInherit(Session):
    @http.route()
    def logout(self, redirect='/web'):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)], limit=1)
        if user:
            # user_data = request.env['user.login.history'].sudo().search(user)
            user_data = request.env['user.login.history'].sudo().search([('user_id', '=', user.id)], limit=1)
            user_data.unlink()
            print(user_data.id)
        return super(SessionInherit, self).logout(redirect=redirect)
