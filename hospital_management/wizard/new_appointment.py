from datetime import date

from odoo.exceptions import ValidationError

from odoo import api, models, fields


class PartnerResend(models.TransientModel):
    _name = 'hospital.appointment.wizard'
    _description = 'Transient model for appointments wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient Name", required=True, ondelete='cascade')
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True, ondelete='cascade')
    appointment_date = fields.Date(string="Appointment Date")
    treatment_end_date = fields.Date(string="End Date")

    @api.model
    def create(self, vals):
        print("Incoming vals:", vals)

        patient_id = vals.get('patient_id')
        appointment_date = vals.get('appointment_date')
        treatment_end_date = vals.get('treatment_end_date')

        if not patient_id:
            raise ValidationError("Patient ID is required.")

        print("Patient ID:", patient_id)
        print("Appointment Date:", appointment_date)

        if appointment_date < date.today().strftime('%Y-%m-%d'):
            raise ValidationError("The appointment date cannot be in the past.")

        if not appointment_date:
            raise ValidationError("Treatment end date is required.")

        if treatment_end_date < appointment_date:
            raise ValidationError("The treatment end date cannot be earlier than the appointment date.")

        existing_appointments = self.env['hospital.appointment'].search(
            [('patient_id', '=', patient_id), ('appointment_date', '=', appointment_date)])
        print("Existing appointments:", existing_appointments)

        if existing_appointments:
            raise ValidationError("The patient already has an appointment on this date.")

        appointment = self.env['hospital.appointment'].create(vals)

        return appointment
