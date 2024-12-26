from odoo import fields, models


class EmployeeReportWizard(models.TransientModel):
    _name = "employee.report.wizard"
    _description = "Print Employee Wizard"

    employee_id = fields.Many2one('wb.employee', string="Employee")
    technology_working_on = fields.Char(related="employee_id.technology_working_on", string="Technology", store=True)

    def action_print_report(self):
        employees = self.env['wb.employee'].search_read([])

        data = {'docids': [emp['id'] for emp in employees], 'docs': employees}

        print(data)
        return self.env.ref('custom_employee.report_employee_document').report_action(self, data=data)
