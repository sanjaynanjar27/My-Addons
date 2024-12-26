import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class SchoolPDFReport(models.TransientModel):
    _name = 'school.pdf.report.model'

    school_ids = fields.Many2one('school.school2', string="School")
    name = fields.Char(related="school_ids.name", string="School Name")


    def action_print_report(self):
        school_id = self.env['school.school2'].browse(self.school_ids.id)
        student_info = {}
        emp_info = {}

        for student in school_id.student_ids:
            student_data = {
                'father_name': student.father_name,
                'birth_date': student.birth_date,
                'gender': student.gender,
                'age': student.age,
                'amount_paid': student.amount_paid,
                'phone': student.phone,
                'email': student.email,
                'sem': student.sem,
                'medium': student.medium,
            }
            student_info[student.id] = student_data

        for emp in school_id.employee_ids:
            employee_data = {
                'name': emp.name,
                'joining_date': emp.joining_date,
                'designation': emp.designation.name,
                'medium_ids': ", ".join(emp.medium_ids.mapped('name')),
                'email': emp.email,
                'phone': emp.phone
            }
            emp_info[emp.id] = employee_data

        data = {
            'name': school_id.name,
            'city': school_id.city,
            'email': school_id.email,
            'phone': school_id.phone,
            'address': school_id.address,
            'fees_amount': school_id.fees_amount,
            'student_info': student_info,
            'emp_info': emp_info,
            'principal': school_id.principal,
            'other_data': 'Some additional data',
        }

        return self.env.ref('school_management.action_school_report_wizard').report_action(self, data=data)

class SchoolConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    state = fields.Selection([('registered', 'Draft'), ('in_process', 'In Progress'), ('confirmed', 'Registered'),
                              ('cancelled', 'Cancelled')], string="state", tracking=True, default='registered')


