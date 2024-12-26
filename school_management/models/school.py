import logging

from odoo.exceptions import ValidationError

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class School(models.Model):
    _name = 'school.school2'
    _description = 'School Information'
    # A short cut used in odoo 17 to skip name_search function customization
    # _rec_names_search = ['name', 'city', 'address', 'phone', 'email']
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    photo = fields.Binary(string="School Photo")
    city = fields.Char(string='City', default='Ahmedabad', tracking=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    address = fields.Text(string="Address", required=True, tracking=True)
    fees_amount = fields.Float(string="Yearly Fees", tracking=True)
    student_ids = fields.One2many('school.student', inverse_name='school_ids', string="Students", tracking=True)
    employee_ids = fields.One2many('school.employees', 'school_id', string="Employees")
    medium_ids = fields.Many2one('school.medium', string="Stream Of Study", tracking=True)
    principal = fields.Char(string="Principal", compute="_compute_principal_name", store=True)
    state = fields.Selection([('registered', 'Draft'), ('in_process', 'In Progress'), ('confirmed', 'Registered'),
                              ('cancelled', 'Cancelled')], string="state", tracking=True, default='registered')
    color = fields.Integer(string="Color Index")

    # token = fields.Float(string="Token Money",
    #                      default=2000,
    #                      required=True)

    # ==================== Inside write function performing vivid tasks on search method  ==================== #

    # =====================
    # Returns School Return Odoo API style edit traditional style or record style
    # =====================

    def _compute_display_name(self):
        for school in self:
            school.display_name = f'{school.name}/{school.email}'

    def student_report(self):
        return {
        }

    def update_state(self):
        self.env['school.school2'].search([]).write({'state': 'registered'})

    @api.returns('school.school2')
    def get_school(self):
        return self

    def open_students(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'school.student',
            'domain': [("school_ids", "=", self.id)],
            'view_mode': 'tree,form',
            'target': 'new', }

    # =====================
    # Validation of email
    # =====================

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if not record.email or "@" not in record.email:
                raise ValidationError("Email must contain '@' symbol.")

    """
    - Adding Search by domain, 
    - search all attributes, using ids property of a record set, and read() function,
    - browse (data).read ( ) - it is used to brows data from id so it should have ids as parameter so it can find data by its value  
    """

    # =====================
    # Write Method
    # =====================

    def write(self, val):
        """print("Value Changed :",val)
        if val['email']:
            if "@" not in val['email']:
                raise ValidationError ("Email must contain '@' symbol.")
            else:
                nv = super (School, self).write (val) """
        nv = super(School, self).write(val)
        for vals in self:
            data_objs = self.env['school.school2'].search([("medium_ids.name", "=", "Hindi")])
            print("Search Domain Data :::: ", type(data_objs))
            for i in data_objs:
                print(i.name, '\n')

            """
            This will be outpur from the search([]) function

             Search Domain Data: : : : <class 'odoo.api.school.school2'>
                school.school2 (8, )
                school.school2 (13, ) """

            data = self.env['school.school2'].search([("medium_ids.name", "=", "Hindi")]).ids
            print("Search Domain Ids :::: ", type(data))
            for i in data:
                print(i, '\n')

                """"
                This will Be output from the search([]).ids operation
                 Search Domain Ids: : : : <class 'list'>
                 8
                 13
                 15 """

            students_data = self.env['school.school2'].browse(data).read()
            print("Brows Data By Id :::: ", type(students_data))
            for i in students_data:
                print(i['email'], '\n')

        """
             Brows Data By Id: : : : <class 'list'> {'id' : 8, 'activity_ids' : [], 'activity_state' : False.....
        """
        return nv

    # =====================
    # Finding Employee With post of Principal
    # =====================

    @api.depends('employee_ids')
    def _compute_principal_name(self):
        for rec in self:
            principal_name = 'Not Available'
            for employee in rec.employee_ids:
                if employee.designation.name == 'Principal':
                    principal_name = employee.name
                    break
            rec.principal = principal_name
            # Debugging output
            print(f"Computed principal for {rec.id}: {principal_name}")

    # =====================
    # name search method
    # =====================
    # @api.model
    # def name_search (self, name='', args=None, operator='ilike', limit=100) :
    #     """ name_search(name='', args=None, operator='ilike', limit=100) -> records
    #
    #     Search for records that have a display name matching the given
    #     ``name`` pattern when compared with the given ``operator``, while also
    #     matching the optional search domain (``args``).
    #
    #     This is used for example to provide suggestions based on a partial
    #     value for a relational field. Should usually behave as the reverse of
    #     ``display_name``, but that is not guaranteed.
    #
    #     This method is equivalent to calling :meth:`~.search` with a search
    #     domain based on ``display_name`` and mapping id and display_name on
    #     the resulting search.
    #
    #     :param str name: the name pattern to match
    #     :param list args: optional search domain (see :meth:`~.search` for
    #                       syntax), specifying further restrictions
    #     :param str operator: domain operator for matching ``name``, such as
    #                          ``'like'`` or ``'='``.
    #     :param int limit: optional max number of records to return
    #     :rtype: list
    #     :return: list of pairs ``(id, display_name)`` for all matching records.
    #     """
    #     ids = self._name_search (name, args, operator, limit=limit, order=self._order)
    #
    #     if isinstance (ids, Query) :
    #         records = self._fetch_query (ids, self._determine_fields_to_fetch (['display_name']))
    #     else :
    #         # Some override of `_name_search` return list of ids.
    #         records = self.browse (ids)
    #         records.fetch (['display_name'])
    #
    #     return [(record.id, record.display_name) for record in records.sudo ( )]
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):  # Here name will be your input key
        args = args or []  # if args contains any input or not it will work
        if name:  # only if you enter the name else your student class logic will be applied
            print("name:", name)
            print("args:", args)
            print("operator:", operator)
            print("Limit:", limit)
            recs = self.search(
                ['|', '|', '|', '|', ('id', operator, name), ('name', operator, name), ('email', operator, name),
                 ('phone', operator, name), ('address', operator, name)], limit=limit).read()
            result = []
            for i in recs:
                entry = (i['id'], f"{i['name']} / {i['email']}")
                result.append(entry)
            print(result)
            return result
        else:
            return super(School, self).name_search(name=name, args=args, operator=operator, limit=limit)


    def action_confirm(self):
        for rec in self:
            rec.state = 'in_process'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params':
                {
                    'title': 'School Registered',
                    'message': 'School has been added for review!',
                    'sticky': False,
                    'type': 'info',
                }}

    def action_register(self):
        self.write({'state': 'confirmed'})

        return {'effect': {'fadeout': 'slow', 'message': 'Congratulations School Is Approved', 'type': 'rainbow_man', }}

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        return {'effect': {'fadeout': 'slow', 'message': 'Cancellation done !', 'type': 'rainbow_man', }}

    def action_closed(self):
        for rec in self:
            rec.state = 'registered'
        print("Action Called")

    def action_test(self):
        return {'type': 'ir.actions.act_url', 'url': 'http://localhost:8069/slides', 'target': 'self', }


class Employees(models.Model):
    _name = 'school.employees'
    _description = 'school staff details and designations'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    photo = fields.Binary(string="Identity")
    joining_date = fields.Date(string="Joining Date", tracking=True)
    designation = fields.Many2one('school.positions', string="Designation", tracking=True)
    school_id = fields.Many2one('school.school2', string="School")
    medium_ids = fields.Many2many('school.medium', string="Stream Of Study", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    phone = fields.Char(string="Phone", tracking=True)


class Designations(models.Model):
    _name = 'school.positions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'school designations'
    name = fields.Char(string="Name")
    employee_id = fields.Many2one('school.employees', string="Employees", tracking=True)


class Stream(models.Model):
    _name = 'school.medium'
    _description = 'School medium of study or mastery'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(name="Name")
    school_ids = fields.One2many('school.school2', inverse_name="medium_ids", string="Schools", tracking=True)

    def write(self, vals):
        self._log_employees()
        return super(Stream, self).write(vals)
