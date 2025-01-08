from odoo import fields, api, models
from odoo.http import request
from odoo.exceptions import UserError


class SelectDateRangeWizard(models.TransientModel):
    _name = 'select.date.range.wizard'
    _inherit = ['startend.mixin']
    _description = 'Select Date Range Wizard'

    report_type = fields.Selection([
        ('xlsx', 'Excel Format'),
        ('pdf', 'PDF Format')
    ], string="Select Report Type", default='pdf')

    def print_report_within_date_range(self):

        if self.report_type == 'xlsx':
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = f"{base_url}/project/task/report/xlsx?start_date={self.start_date}&end_date={self.end_date}"
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
        elif self.report_type == 'pdf':
            task_info = []
            task_ids = request.env['project.task'].search([
                ('create_date', '>=', self.start_date),
                ('create_date', '<=', self.end_date)
            ])
            for task_id in task_ids:
                user_info = {
                    'name': task_id.user_id.name if task_id.user_id else "No User ID Found"
                }

                company_info = {
                    'name': task_id.company_id.name if task_id.company_id else "No Company ID Found",
                    'email': task_id.company_id.email if task_id.company_id else "No Email Found",
                    'phone': task_id.company_id.phone if task_id.company_id else "No Phone Found",
                }

                project_info = {}
                if task_id.project_id:
                    project = task_id.project_id
                    project_info = {
                        'company_id': project.company_id.name if project.company_id else "No Company ID Found",
                        'date_start': project.date_start if project.date_start else "No Start Date",
                        'date': project.date if project.date else "No Date",
                        'description': project.description if project.description else "No Description",
                        'team_name': project.team_name if hasattr(project,
                                                                  'team_name') and project.team_name else "No Team Name",
                    }
                else:
                    project_info = {
                        'company_id': "No Project Found",
                        'date_start': "No Start Date",
                        'date': "No Date",
                        'description': "No Description",
                        'team_name': "No Team Name",
                    }

                data = {
                    'user_id': user_info,
                    'company_id': company_info,
                    'name': task_id.name,
                    'project_info': project_info,  # Include project information
                }
                task_info.append(data)  # Append the task data to the list

            print(task_info)  # Debug output to check the gathered data
            return self.env.ref('project_custom.action_project_task_report').report_action(self,
                                                                                           data={'tasks': task_info})
        else:
            raise UserError('Please select a report type.')
