from odoo import api, models, fields
from odoo.exceptions import ValidationError


class AbstractStartEndDateMixin(models.AbstractModel):
    _name = 'startend.mixin'
    _description = 'Mixin for models with start and end dates'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.constrains('start_date', 'end_date')
    def _check_date_order(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError("Start date cannot be after end date.")


class ProjectCustom(models.Model):
    _name = 'project.custom'
    _description = 'Custom Project'
    _inherit = ['startend.mixin']

    name = fields.Char(string='Custom Project Name')
    task_ids = fields.Many2many('project.task', string='Tasks')
