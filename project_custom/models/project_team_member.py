from odoo import api, fields, models
import base64
from io import BytesIO
from PIL import Image

class ProjectTeamMember(models.Model):
    _name = 'project.team.member'
    _description = 'Project Team Member Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = {
        ('project_team_restrict_duplicates', 'UNIQUE(name)', 'You Can Not Copy User Information'),
        ('project_team_restrict_duplicate_phone', 'UNIQUE(mobile)', 'Not Valid Phone'),
    }

    name = fields.Char(string='Name', required=True)
    member_email = fields.Char(string='Member Email', required=True)
    address = fields.Char(string='House Number', required=True)
    street = fields.Char(string="Street")
    street2=fields.Char(string="Street2")
    country_id = fields.Many2one("res.country", string="Country")
    state_id = fields.Many2one(
        "res.country.state", string="State",
        domain="[('country_id', '=?', country_id)]")
    city = fields.Many2one('res.state.cities',string="City",domain="[('state_id', '=?', state_id),('country_id', '=?', country_id)]")
    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
    )
    email = fields.Char(
        related="user_id.login",
        string="User Email",
    )
    mobile = fields.Char(string="Phone")
    zip = fields.Char(string="Zip")
    gender = fields.Selection([('male','Male'),('female','Female')], required = True)
    date_of_birth = fields.Date(string="Date of Birth")
    photo = fields.Binary(string="Upload Identity")
    info = fields.Html(string="Bio Data")
    is_active = fields.Boolean("Is Active?")
    timesheet_ids = fields.One2many('account.analytic.line',inverse_name="team_member_id",string='Associated Timesheets')
    activity_ids = fields.One2many('mail.activity', 'res_id', string="Activities",
                                   domain=[('res_model', '=', 'project.team.member')])

    def search_default_employee(self):
        return [('user_id', '=', 2)]

    def create(self, vals):
        res = super(ProjectTeamMember, self).create(vals)
        if vals.get('name'):
            user = self.env['res.users'].create({'name': vals['name'],'login': vals['name']})
        return res


class CountryStateCities(models.Model):
    _name = 'res.state.cities'
    _description = 'Country State and Cities'
    country_id = fields.Many2one("res.country", string="Country")
    state_id = fields.Many2one(
        "res.country.state", string="State",
        domain="[('country_id', '=?', country_id)]")
    name = fields.Char(string="Name")


class TimeSheetInverseModel(models.Model):
    _inherit = 'account.analytic.line'
    team_member_id = fields.Many2one('project.team.member',inverse = "timesheet_ids", string='Team Member')

