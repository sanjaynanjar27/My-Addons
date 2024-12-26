import logging

from odoo.exceptions import UserError

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Appointments(models.Model):
    _name = "hospital.appointment"
    _description = "All details about appointment"
    _inherit = ["mail.thread", 'mail.activity.mixin']

    reference = fields.Char(string='Reference', default="New", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", widget="many2one")

    name = fields.Char(related='doctor_id.name')

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_date = fields.Datetime(string='Appointment Date')
    treatment_end_date = fields.Datetime(string="End Date")
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string='Priority',
                                track_visibility='onchange')

    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', string='Status', required=True, track_visibility='always')

    report_id = fields.Many2one('custom.report', string='Report')

    @api.model
    def create(self, vals):
        _logger.info("Appointment Has Been Booked _____________________: %s", vals)

        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('seq.appointment')

        print(vals.get('reference'))

        return super(Appointments, self).create(vals)

    @api.model
    def action_confirm(self):
        patients = self.env['hospital.patient'].search([])
        _logger.info("Appointment Has Been Booked _____________________: %s", patients)

    def confirm_appointment(self):
        self.write({'state': 'in_consultation'})
        return {
            'effect': {'fadeout': 'slow', 'message': ' Process Forwarded to Consultation !', 'type': 'rainbow_man', }}

    def appointment_over(self):
        self.write({'state': 'done'})
        return {'effect': {'fadeout': 'slow', 'message': ' Consultation Process Done!', 'type': 'rainbow_man', }}

    def cancel_appointment(self):
        if self.state == "done":
            raise UserError("After Completion of Appointment You can not cancel it.")
        self.write({'state': 'cancel'})
        return {'effect': {'fadeout': 'slow', 'message': ' Cancelled !', 'type': 'rainbow_man', }}

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            if record.appointment_date and record.appointment_date < fields.Datetime.now():
                raise UserError("The appointment date cannot be in the past.")
