from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string='Team', domain="[('is_active', '=', True)]")
    members = fields.Many2many(
        'project.team.member',
        string='Team Members',
        compute='_compute_members',
        store=True
    )

    @api.depends('team_id')
    def _compute_members(self):
        for project in self:
            if project.team_id:
                project.members = project.team_id.team_members
            else:
                project.members = False
