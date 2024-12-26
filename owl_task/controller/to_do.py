from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/task/list', website=True, auth="public")
    def add_to_list(self, **key):
        return request.render('owl_task.my_template',{})