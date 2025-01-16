import logging

from odoo.exceptions import UserError

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = "hospital.doctor"
    _description = "About Doctor"
    _inherit = ["mail.thread"]

    initial_id = fields.Many2one('name.initials',string="Initial")
    name = fields.Char(string="Doctor", tracking=True)
    expertise = fields.Char(string="Expertise", tracking=True)
    image = fields.Binary(string="Image")
    experience = fields.Integer(string="Experience", tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string="Appointments")
    experience_display = fields.Char(compute='_compute_experience_display', string='Experience')

    def create(self, vals):
        if vals['name'] == '' or not vals.get('name'):
            raise UserError("Must Enter Name..")
        return super().create(vals)

    def _compute_experience_display(self):
        for record in self:
            record.experience_display = f"{record.experience} years" if record.experience else "N/A"

    @api.model
    def write(self, vals):
        return super(Doctor, self).write(vals)


class Users(models.Model):
    _inherit = 'res.users'

    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
