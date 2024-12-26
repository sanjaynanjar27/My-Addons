from odoo import http
from odoo.http import request


class SalesDashboardController(http.Controller):

    @http.route('/get_data', type='http', auth='user')
    def get_data(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_message',
            'params':
                {
                    'title': 'School Registered',
                    'message': 'School has been added for review!',
                    'sticky': False,
                    'type': 'info',
                }}


