from odoo import http
from odoo.http import request
from io import BytesIO
import xlsxwriter
from odoo.exceptions import UserError


class ProjectTaskReportController(http.Controller):

    @http.route('/crm_lead', auth='public', website=True)
    def web_form(self, **kwargs):
        partner_ids = request.env['res.partner'].sudo().search([])
        return request.render('project_custom.web_form_template', {'partner_ids': partner_ids})

    @http.route('/crm/crm_lead_form/', type='http', auth='public', methods=['POST'], csrf=True, website=True)
    def submit_form(self, **args):
        name = args.get('name')
        partner_id = int(args.get('partner', 0))
        email_from = args.get('email')
        phone = args.get('phone')
        probability = args.get('probability')
        expected_revenue = args.get('expected_revenue')
        print(name, email_from, probability, partner_id, phone)

        result = request.env['crm.lead'].sudo().create({
            'name': name,
            'partner_assigned_id': partner_id,
            'email_from': email_from,
            'phone': phone,
            'probability': probability,
            'expected_revenue': expected_revenue
        })

        if result:
            return request.redirect('/contactus-thank-you')
        else:
            UserError("Data Not Submitted")

    @http.route('/project/task/report/xlsx', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_xlsx_report(self, **kwargs):
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        if not start_date or not end_date:
            return "Please provide start and end dates."

        task_ids = request.env['project.task'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date)
        ])

        task_info = []
        for task in task_ids:
            user_info = {
                'name': task.user_id.name if task.user_id else "No User ID Found"
            }
            company_info = {
                'name': task.company_id.name if task.company_id else "No Company ID Found",
                'email': task.company_id.email if task.company_id else "No Email Found",
                'phone': task.company_id.phone if task.company_id else "No Phone Found",
            }

            project_info = {
                'company_id': task.project_id.company_id.name if task.project_id and task.project_id.company_id else "No Company ID Found",
                'date_start': task.project_id.date_start if task.project_id and task.project_id.date_start else "No Start Date",
                'date': task.project_id.date if task.project_id and task.project_id.date else "No Date",
                'description': task.project_id.description if task.project_id and task.project_id.description else "No Description",
                'team_name': task.project_id.team_name if hasattr(task.project_id,
                                                                  'team_name') and task.project_id.team_name else "No Team Name",
            }

            task_info.append({
                'name': task.name,
                'user_id': user_info,
                'company_id': company_info,
                'project_info': project_info,
            })

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Task Report')

        header_format = workbook.add_format(
            {'bold': True, 'bg_color': '#D3D3D3', 'align': 'center', 'valign': 'vcenter'})

        worksheet.write('A1', 'Task Name', header_format)
        worksheet.write('B1', 'User', header_format)
        worksheet.write('C1', 'Company', header_format)
        worksheet.write('D1', 'Email', header_format)
        worksheet.write('E1', 'Phone', header_format)
        worksheet.write('F1', 'Project', header_format)
        worksheet.write('G1', 'Start Date', header_format)
        worksheet.write('H1', 'Project Date', header_format)
        worksheet.write('I1', 'Description', header_format)
        worksheet.write('J1', 'Team Name', header_format)

        row = 1
        for task in task_info:
            worksheet.write(row, 0, task['name'])
            worksheet.write(row, 1, task['user_id']['name'])
            worksheet.write(row, 2, task['company_id']['name'])
            worksheet.write(row, 3, task['company_id']['email'])
            worksheet.write(row, 4, task['company_id']['phone'])
            worksheet.write(row, 5, task['project_info']['company_id'])
            worksheet.write(row, 6, task['project_info']['date_start'])
            worksheet.write(row, 7, task['project_info']['date'])
            worksheet.write(row, 8, task['project_info']['description'])
            worksheet.write(row, 9, task['project_info']['team_name'])
            row += 1

        workbook.close()
        output.seek(0)

        response = request.make_response(
            output.read(),
            headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                     ('Content-Disposition', 'attachment; filename="task_report.xlsx"')]
        )

        return response
