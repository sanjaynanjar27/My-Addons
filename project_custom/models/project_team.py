from odoo import api, models, fields
from datetime import date


class ProjectTeam(models.Model):
    _name = 'project.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project Team Module Documentation'

    # add reference for team name 001/name/date
    reference = fields.Char('Code', default='New', trace=True, copy=False)
    name = fields.Char(string='Team Name', required=True)
    team_members = fields.Many2many('project.team.member', required=True, string="Team Members In Team", tracking=True)
    team_leader = fields.Many2one('res.users', required=True, string="Team Leader")
    is_active = fields.Boolean(string='Is Active', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            sequence_prefix = self.env['ir.sequence'].next_by_code('project.team.reference.1')
            current_date = date.today().strftime("%Y%m%d")
            vals['reference'] = f'{sequence_prefix}/{vals["name"]}/{current_date}'
            return super(ProjectTeam, self).create(vals)

    def open_team_members(self):
        return {
            'name': 'Team Members',
            'type': 'ir.actions.act_window',
            'res_model': 'project.team.member',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.team_members.ids)],
            'target': 'current',
        }

    @api.model
    def add_user_to_selected_teams(self):
        active_ids = self.env.context.get('active_ids', [])
        selected_teams = self.env['project.team'].browse(active_ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Team Members',
            'res_model': 'project.team.add.member.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
        # if not active_ids:
        #     raise ValueError("No teams selected to add the member.")
        # print(active_ids)
        # print(selected_teams.team_members)
        # member_id = self.env['project.team.member'].search([('name', '=', 'Sample User')], limit=1)
        #
        # if not member_id:
        #     raise ValueError("The member was not found.")
        #
        # for team in selected_teams:
        #     if member_id not in team.team_members:
        #         team.team_members = [(4, member_id.id)]  # 4 means "add" in Many2many fields
