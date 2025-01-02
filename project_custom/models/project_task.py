from odoo import api, models, fields
from odoo.exceptions import ValidationError,UserError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class ProjectTasks(models.Model):
    _inherit = 'project.task'
    _order = 'name asc'


    user_id = fields.Many2one('res.users', string="Assigned User")
    is_state_visible = fields.Boolean(compute='_compute_is_state_visible', store=True)

    @api.model
    def send_deadline_alert(self):
        tasks = self.env['project.task'].search([("date_deadline", "!=", False), ("project_id", "!=", False)])

        for task in tasks:
            # Prepare a list of team member emails
            member_emails = [member.email for member in task.project_id.team_id.team_members if member.email]

            # Prepare context for the email template
            if member_emails:
                confirm_action_url = "some_url_here"  # Generate the URL or keep it empty if not required
                template = self.env.ref('project_custom.email_template_task_deadline_warning')
                template.with_context({
                    'task_name': task.name,
                    'project_name': task.project_id.name,
                    'deadline': datetime.today(),
                    'member_names': ', '.join([member.name for member in task.project_id.team_id.team_members]),
                    'token_url': confirm_action_url
                }).send_mail(
                    task.id,
                    email_layout_xmlid='mail.mail_notification_light',
                    email_values={
                        'author_id': self.create_uid.partner_id.id,
                        'auto_delete': True,
                        'email_from': self.env.company.email_formatted,
                        'email_to': ', '.join(member_emails),
                        'message_type': 'user_notification',
                    },
                    force_send=True,
                )

            _logger.info(f"Sending deadline alert of DATE ... {task.date_deadline.date()} to user {task.user_ids}")

            # Message to be posted to task's message log (only once)
            message = (
                f"Reminder: The task '{task.name}' in project '{task.project_id.name}' "
                f"has a deadline today ({task.date_deadline}). Please ensure timely completion."
            )

            # Post message on the task's message log
            task.message_post(
                body=message,
                subtype_id=self.env.ref('mail.mt_note').id,
            )

            # Post message to all team members' message logs (only once)
            for user in task.project_id.team_id.team_members:
                if user.email:  # Ensure the user has an email
                    user.message_post(
                        body=message,
                        subtype_id=self.env.ref('mail.mt_note').id,
                    )

    @api.depends('state')
    def _compute_is_state_visible(self):
        print(f"For State Update ID: {self.state}")
        if self.state == '1_done':
            self.date_end = datetime.now()
        else:
            self.date_end = False

        for task in self:
            task.is_state_visible = task.state != '1_done'


    def unlink(self):
        if self.state == '01_in_progress':
            raise UserError("Can not delete Task while it's Under Progress!")
        return super(ProjectTasks, self).unlink()


    @api.model
    def add_priority_to_multiple_tasks(self):
        active_ids = self.env.context.get('active_ids', [])
        print(active_ids)
        selected_tasks = self.env['project.task'].browse(active_ids)
        selected_tasks.priority = '1'
        print(selected_tasks)
