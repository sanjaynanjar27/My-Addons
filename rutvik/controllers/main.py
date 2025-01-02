from odoo import http
from odoo.http import request

class UserInputController(http.Controller):

    @http.route('/user_input/data',type='http', auth="public", website=True, sitemap=False)
    def user_input(self, **kwargs):
        response = request.render('rutvik.user_input_template', {})
        return response
