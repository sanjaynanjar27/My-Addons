from odoo import models, fields, api
from odoo.exceptions import UserError

class HospitalDoctorReportWizard(models.TransientModel):
    _name = 'hospital.doctor.report.wizard'
    _description = 'Hospital Doctor Report Wizard'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detailed', 'Detailed')],
        string='Report Type',
        default='summary'
    )

    def print_report(self):
        self.ensure_one()
        doctor_id = self.env['hospital.doctor'].browse(self.doctor_id.id)
        appointment_info = {}
        total_appointments = 0

        for appointment in self.doctor_id.appointment_ids:
            appointment_data = {
                'reference' : appointment.reference,
                'appointment_date' : appointment.appointment_date,
                'treatment_end_date' : appointment.treatment_end_date,
                'priority' : appointment.priority,
                'patient_name' : appointment.patient_id.name
            }
            appointment_info[appointment.id] = appointment_data
            total_appointments += 1

        report_type = self.report_type
        data = {
            'name':doctor_id.name,
            'expertise':doctor_id.expertise,
            'experience' : doctor_id.experience,
            'appointment_info' : appointment_info,
            'report_type': report_type,
            'total_appointments':total_appointments
        }
        return self.env.ref('hospital_management.report_doctor_wizard').report_action(self, data=data)