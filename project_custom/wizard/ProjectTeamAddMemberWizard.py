from odoo import models, fields,api
from odoo.exceptions import ValidationError
from odoo.http import request

class ProjectTeamAddMemberWizard(models.TransientModel):
    _name = 'project.team.add.member.wizard'
    _description = 'Add Member to Selected Teams Wizard'

    member_id = fields.Many2one('project.team.member', string="Team Member", required=True)


    def add_member(self):
        team_ids = self.env.context.get('active_ids', [])
        selected_teams = self.env['project.team'].browse(team_ids)
        print('selected teams' , selected_teams)
        print('==',selected_teams.team_members)
        print('==',self.member_id)
        if self.member_id:
            if  self.member_id in selected_teams.team_members:
                raise ValidationError('Member already exists in One the selected teams.')
            else:
                selected_teams.team_members = [(4, self.member_id.id)]
                print(self.member_id)
        else:
            raise ValueError('No Member Selected')