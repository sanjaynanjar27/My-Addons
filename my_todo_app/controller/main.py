# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import http
from odoo.http import request

class MyAppController(http.Controller):


    @http.route('/my_app_todo', type='http', auth="public", website=True, sitemap=False)
    def todo_app(self, **kwargs):
        return request.render('my_todo_app.button_with_todo_list', {})
