from odoo import api, models, fields
from datetime import date

class ProjectTeam(models.Model):
    _name = 'project.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project Team Module Documentation'

    # add reference for team name 001/name/date
    reference = fields.Char('Code',default='New', trace=True, copy=False)
    name = fields.Char(string='Team Name', required=True)
    team_members = fields.Many2many('project.team.member', required=True, string="Team Members In Team",tracking=True)
    team_leader = fields.Many2one('res.users', required=True, string="Team Leader")
    is_active = fields.Boolean(string='Is Active', required=True,tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            sequence_prefix = self.env['ir.sequence'].next_by_code('project.team.reference.1')
            current_date = date.today().strftime("%Y%m%d")
            vals['reference'] = f'{sequence_prefix}/{vals["name"]}/{current_date}'
            return super(ProjectTeam, self).create(vals)

