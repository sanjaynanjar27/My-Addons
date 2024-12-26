from odoo.http import request

from odoo import http


class School(http.Controller):

    @http.route('/school/schools', website=True, auth="public")
    def school_data(self, **key):
        schools = request.env['school.school2'].sudo().search([])
        return request.render("school_management.school_page", {'schools': schools})

    @http.route('/hospital/appointment', website=True, auth="user")
    def hospital_doctor(self, **key):
        appointments = request.env['hospital.appointment'].sudo().search([])
        return request.render('school_management.report_pdf_template_url', {'appointments': appointments})
