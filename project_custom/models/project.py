from odoo import fields, models, api
from odoo.exceptions import AccessError

class Project(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string='Project Team  ', required=True, ondelete="cascade")
    team_name = fields.Char(related='team_id.name', string='Team Name',store=True)
    team_leader_name = fields.Char(related='team_id.team_leader.login', string='Team Leader Name')
    team_member_names = fields.Char(string="Team Members", compute="_compute_team_members")

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('project.group_project_manager') and not self.env.user.has_group(
                'base.group_system'):
            raise AccessError("Only Project Managers and Administrators can create teams.")
        return super(Project, self).create(vals)

    @api.depends('team_id.team_members')
    def _compute_team_members(self):
        for record in self:
            if record.team_id and record.team_id.team_members:
                member_names = record.team_id.team_members.mapped('name')  # Assuming `name` is the field in 'project.team.member'
                record.team_member_names = ', '.join(member_names)
            else:
                record.team_member_names = ''

 # 25 <= 26 <= 30