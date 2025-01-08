from odoo import api, models, fields, exceptions

class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    team_member_id = fields.Many2one('project.team.member', string='Team Member')

    @api.model
    def create(self, vals):
        # Create the timesheet record
        record = super(AnalyticLine, self).create(vals)

        if record.task_id and record.employee_id:
            task = record.task_id
            project = task.project_id

            team_member = self.env['project.team.member'].search([
                ('user_id', '=', record.employee_id.user_id.id),
                ('is_active', '=', True)
            ], limit=1)

            if not team_member:
                team_member = self.env['project.team.member'].create({
                    'name': record.employee_id.name,
                    'user_id': record.employee_id.user_id.id,
                    'member_email': record.employee_id.work_email,
                    'mobile': record.employee_id.mobile_phone,
                    'gender': 'male',
                    'is_active': True,
                })

            record.team_member_id = team_member.id

            if project and team_member.user_id not in project.user_ids:
                project.write({'user_ids': [(4, team_member.user_id.id)]})

        return record
