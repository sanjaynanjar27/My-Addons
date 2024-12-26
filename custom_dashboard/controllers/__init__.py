from odoo import http
from odoo.http import request

class CustomDashboardController(http.Controller):
    @http.route('/dashboard/owl', auth='user', website=True)
    def render_dashboard(self):
        return request.render('custom_dashboard_owl.view_dashboard_owl')
