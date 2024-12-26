# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import functools
import werkzeug
from datetime import datetime, timedelta
from odoo.http import root, request, Session, Application, FilesystemSessionStore, FutureResponse
from odoo.tools import config, func
from odoo.tools.func import lazy_property


@functools.wraps(werkzeug.Response.set_cookie)
def set_cookie(self, key, value='', max_age=None, expires=-1, path='/',
    domain=None, secure=False, httponly=False, samesite=None, cookie_type='required'):
    if expires == -1:  # default value (1 year)
        expires = datetime.now() + timedelta(days=365)
    if request.env.uid:
        user = request.env['res.users'].browse(request.env.uid)
        if user and user.is_session_expire and user.session_expire_limit > 0:
            max_age = int(user.session_expire_limit) or max_age
    if request.db and not request.env['ir.http']._is_allowed_cookie(cookie_type):
        max_age = 0  # Reset if not allowed

    werkzeug.Response.set_cookie(self, key, value=value, max_age=max_age, expires=expires,
        path=path, domain=domain, secure=secure, httponly=httponly, samesite=samesite)


class OpenERPSession(Session):
    
    def logout(self,keep_db=False):
        if self.sid and keep_db:
            session = request.env['res.users.logger'].sudo().search(
                [('session_id','=',self.sid)])
            if session:
                session._on_logout()
        return super(OpenERPSession,self).logout(keep_db=keep_db)


class FilesystemSessionStore(FilesystemSessionStore):

    def rotate(self, session, env):
        res = super().rotate(session, env)
        request.env['res.users.logger'].sudo().save_session()
        return res


class Application(Application):

    @func.lazy_property
    def session_store(self):
        # Setup http sessions
        path = config.session_dir
        return FilesystemSessionStore(path, session_class=OpenERPSession)


root.session_store = Application().session_store
root.rotate = FilesystemSessionStore().rotate
FutureResponse.set_cookie = set_cookie