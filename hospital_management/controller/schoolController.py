import io
from datetime import datetime

import xlsxwriter
from odoo.http import request

from odoo import fields
from odoo import http


class SchoolController(http.Controller):

    @http.route('/hospital/doctors', website=True, auth="user")
    def hospital_doctor(self, **key):
        doctors = request.env['hospital.doctor'].sudo().search([])
        return request.render('hospital_management.doctor_page', {'doctors': doctors})

    @http.route('/report/xlsx/custom_report', type='http', auth='user')
    def generate_patient_xlsx_report(self):
        patients = request.env['hospital.patient'].sudo().search([])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Patient Report")
        bold = workbook.add_format({'bold': True})
        worksheet.write(0, 0, 'Patient Name', bold)
        worksheet.write(0, 1, 'Age', bold)
        worksheet.write(0, 2, 'Gender', bold)
        worksheet.write(0, 3, 'Birth Date', bold)
        worksheet.write(0, 4, 'Phone', bold)
        worksheet.write(0, 5, 'Water Level', bold)
        worksheet.write(0, 6, 'Heart Rate', bold)
        worksheet.write(0, 7, 'Disability', bold)
        worksheet.write(0, 8, 'Address', bold)

        row = 1
        for patient in patients:
            age = self.calculate_age(patient.date_of_birth) if patient.date_of_birth else ''

            worksheet.write(row, 0, patient.name or '', bold)
            worksheet.write(row, 1, age)
            worksheet.write(row, 2, '')
            worksheet.write(row, 3, 'N/A')
            worksheet.write(row, 4, patient.phone or '')
            worksheet.write(row, 5, patient.walter_level or '')
            worksheet.write(row, 6, patient.heart_rate or '')
            worksheet.write(row, 7, 'Yes' if patient.disabled else 'No')
            worksheet.write(row, 8, patient.address or '')
            row += 1
        workbook.close()
        output.seek(0)

        return request.make_response(output.read(), headers={
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': 'attachment; filename="patient_report.xlsx"', })

    def calculate_age(self, dob):
        if not dob:
            return ''

        today = datetime.today()
        dob_date = fields.Date.from_string(dob)
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return age
