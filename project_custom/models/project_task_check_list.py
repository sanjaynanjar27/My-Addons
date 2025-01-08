from odoo import api, models, fields


class ProjectTaskCheckList(models.Model):
    _name = 'project.task.checklist'
    _description = 'Project Task Checklist'
    _inherit = ['startend.mixin']

    task_id = fields.Many2one('Project Task', required=True)
