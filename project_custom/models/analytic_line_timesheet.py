from odoo import api, models, fields


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        record = super(AnalyticLine, self).create(vals)

        if record.task_id:
            task = record.task_id
            project = task.project_id
            employee = record.employee_id
            if employee and project:
                if employee.user_id not in project.user_ids:
                    project.write({'user_ids': [(4, employee.user_id.id)]})

        return record
