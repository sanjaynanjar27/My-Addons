import logging
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api

# Configure logging
_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _name = 'wb.employee'
    _description = 'Custom Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    reference = fields.Char(string="Emp ID", default="New", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], required=True, track_visibility="onchange",
                              index=True)
    name = fields.Char(string='Name', required=False, copy=False, index=True)
    email = fields.Char(string='Email', required=True, track_visibility='always', default="@gmail.com", index=True)
    phone_number = fields.Char(string='Phone Number', required=True)
    currency_id = fields.Many2one('res.currency', 'Currency')
    salary = fields.Monetary(string='Salary')
    joining_year = fields.Char(string='Joining Year')
    technology_working_on = fields.Char(string='Technology Working On', track_visibility='onchange')
    hobby_ids = fields.Many2many('wb.hobby', string='Hobbies', help='Select hobbies associated with the employee.')
    phone_number_to_disp = fields.Char(compute="_compute_phone_number_digit", string="Phone Number")
    birth_date = fields.Date(string="Birth Date", track_visibility='onchange')
    age = fields.Char(compute="_compute_age_from_birthdate", inverse="_inverse_age", search="_search_age", string="Age",
                      store=True)
    upper_name = fields.Char(compute="_compute_upper_name", string="Name", store=False)

    def copy(self, default=None):
        res = super(Employee, self).copy(default)
        _logger.info("Copied Values Are %s", res.read())
        return res

    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('emp.number')

        emp = super(Employee, self).create(vals)
        _logger.info('Employee Entered: %s', emp.name)
        return emp

    def write(self, vals):
        employees = super(Employee, self).write(vals)
        _logger.info('Employee Value Changed: %s', employees)
        for i in self:
            data = self.env['wb.employee'].search([('gender', '=', 'female')]).ids
            data_vals = self.env['wb.employee'].browse(data).read()
            print(data_vals)
        return employees

    @api.model
    def _search_age(self, operator, value):
        birth_date = date.today() - relativedelta(years=int(value))
        start_date = birth_date.replace(day=1, month=1)
        end_date = birth_date.replace(day=31, month=12)
        print("________________________", birth_date, 'Start Date  : ', start_date, 'End Date : ', end_date)
        _logger.info("Birth Year Will Be From this Date :", birth_date)
        return [("birth_date", ">=", start_date), ("birth_date", "<=", end_date)]

    @api.depends('name')
    def _compute_upper_name(self):
        for record in self:  # Iterate over each record
            record.upper_name = record.name.upper() if record.name else "N/A"

    @api.depends('birth_date')
    def _compute_age_from_birthdate(self):
        for record in self:
            if record.birth_date:
                birth_date = fields.Date.from_string(record.birth_date)
                today = date.today()
                age = today.year - birth_date.year
                record.age = str(age)
            else:
                record.age = "N/A"

    @api.depends('age')
    def _inverse_age(self):
        for record in self:
            if record.age and record.age != "N/A":
                current_year = date.today().year
                age = int(record.age)
                birth_year = current_year - age
                if record.birth_date:
                    original_birth_date = fields.Date.from_string(record.birth_date)
                    print(original_birth_date)
                    birth_date = date(birth_year, original_birth_date.month, original_birth_date.day)
                    print(birth_date)
                else:
                    birth_date = date(birth_year, 1, 1)
                record.birth_date = fields.Date.to_string(birth_date)
                print(record.birth_date, "_________________-")
            else:
                record.birth_date = "N/A"

    @api.depends('phone_number')
    def _compute_phone_number_digit(self):
        for rec in self:
            rec.phone_number_to_disp = f"+91 {rec.phone_number}" if rec.phone_number else "N/A"


class Hobby(models.Model):
    _name = 'wb.hobby'
    name = fields.Char(string='Hobby Name', ondelete="restrict")
    description = fields.Text(string='Description')


"""

In Odoo's QWeb templating engine, the t-att attribute is used to dynamically set HTML attributes based on the context.
It allows you to assign a value to an HTML element's attribute in a flexible and data-driven way.
This is especially useful when you need to generate dynamic content based on the model data.

t-att=mapping : 

The t-att=mapping is used when you want to assign multiple attributes to an element dynamically. 
The value of mapping should be a Python dictionary, where the keys are the attribute names, and the values are the attribute values to be set.

        <t-foreach="records" t-as="record">
            <div t-att="{'class': record.class_name, 'style': 'color: ' + record.color}">
                <!-- Your content here -->
            </div>
        </t-foreach>

In this example, t-att dynamically assigns multiple attributes (class and style) based on the data in the record.

t-att=pair
The t-att=pair is similar but works with a single attribute-value pair. 
It assigns a single attribute to an HTML element, where pair refers to a dictionary with a single key-value pair.

Example:

xml
Copy code
        <t-foreach="records" t-as="record">
            <span t-att="{'title': record.tooltip}">
                <span t-esc="record.name"/>
            </span>
        </t-foreach>


In this example, the title attribute of the <span> is dynamically set to the value of record.tooltip.

Summary:
    t-att=mapping: Sets multiple attributes dynamically using a dictionary,
     where each key-value pair corresponds to an attribute and its value.
    t-att=pair: Sets a single attribute dynamically using a dictionary with one key-value pair.
    Both of these approaches help you create more flexible and dynamic HTML in your QWeb templates,
     reducing the need to hard-code values and improving the adaptability of your views.

"""
