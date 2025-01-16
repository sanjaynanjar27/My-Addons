import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Master'
    _inherit = ["mail.thread"]

    reference = fields.Char(strign="Reference", default="New")
    initial_id = fields.Many2one('name.initials',strign="Initial")
    name = fields.Char(string="Name", required=True, tracking=True)
    phone = fields.Char(string="Phone Number", required=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True, widget="radio")
    heart_rate = fields.Integer(string="Heart Rate", tracking=True)
    walter_level = fields.Float(string="Water Level", tracking=True)
    visiting_time = fields.Datetime(string="Time", tracking=True)
    disabled = fields.Boolean(string="Any Disability?", tracking=True)
    prev_reports = fields.Binary(string="Upload your previous medical history reports", tracking=False)
    address = fields.Html(string="You can enter data in HTML Form", tracking=True, widget="html")
    notes = fields.Text(string="Write Prescriptions and Notes", tracking=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', "patient_id", string="Appointments")
    state = fields.Selection([('draft','New'),('waiting','Waiting'),('in_appointment','On Going'),('cancelled','Cancelled'),('done','Done')],string='State')

    @api.model
    def create(self, vals):
        _logger.info("Creating a new patient with values: %s", vals)

        if not vals.get('reference') or vals['reference'] == "New":
            vals['reference'] = self.env['ir.sequence'].next_by_code('patient.seq')

        patient = super(Patient, self).create(vals)

        appointment_vals = {'doctor_id': patient.doctor.id, 'patient_id': patient.id,
                            'appointment_date': fields.Datetime.now(), 'state': 'draft', }
        self.env['hospital.appointment'].create(appointment_vals)
        _logger.info("Appointment created for patient: %s", patient.name)

        return patient

    def open_appointments(self):
        return {'type': 'ir.actions.act_window', 'name': 'Appointments', 'res_model': 'hospital.appointment',
                'domain': [("patient_id", "=", self.id)], 'view_mode': 'tree,form', 'target': 'current', }

    def action_new_appointment(self):
        self.ensure_one()

        return {'name': 'New Appointment', 'view_mode': 'form', 'res_model': 'hospital.appointment.wizard',
                'type': 'ir.actions.act_window', 'context': {'default_patient_id': self.id},
                'domain': [("patient_id", "=", self.id)], 'target': 'new', }

    def generate_patient_xlsx_report(self):
        return {'type': 'ir.actions.act_url', 'url': 'http://localhost:8069/report/xlsx/custom_report',
                'target': 'self', }
