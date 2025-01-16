import logging
from datetime import date

from odoo.exceptions import ValidationError

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Students(models.Model):
    _name = 'school.student'
    _description = 'About students'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sequence.mixin']
    _rec_names_search = ['name', 'father_name']  # Default Name Search
    _sql_constraints = [  # ('unique_en_number', 'unique(en_number)',
        #  "Enrollment Number Already Exists. Please Enter a Unique Number"),
        ('email_validation', 'unique(email)', 'Email Already Exists.'), ('check_age_validity', 'CHECK(age >= 5)',
                                                                         'Age must be more than 4 years to register and less than or equal to 100.'),
        ('check_amount_if_school', 'CHECK((school_ids IS NULL) OR (amount_paid > 0))',
         'Amount Paid must be greater than zero if a School is selected.')]

    """ 
    _sql_constraints = [('name_for_condition','condition logic','Message Warning to display')]
    """

    reference = fields.Char(string='Reference', default="New")
    name = fields.Char(string="Name", required=True, default="John Doe", tracking=True)  # default name will be John Doe
    photo = fields.Binary(string="Identity")  # Can upload image here
    birth_date = fields.Date(string="Birth Date", required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male', tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age_from_date", search="_search_student_by_age", tracking=True,
                         store=True)  # compute field attribute
    amount_paid = fields.Float(string="Amount Paid", help="Only for students who partly paid their fees",
                               required=False, tracking=True)
    father_name = fields.Char(string="Fathers Name", required=True, tracking=True)
    phone = fields.Char(string="Contact Number", help="Must Be active phone number", tracking=True)
    email = fields.Char(string="Email ID", required=True, tracking=True)
    sem = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')],
        string="Semester", tracking=True)
    medium = fields.Selection([('English', 'English'), ('Hindi', 'Hindi'), ('Gujarati', 'Gujarati')],
                              string="Study Stream", default='Hindi',
                              help="You must select Study Stream To Select The School",
                              tracking=True)  # Default stream will be selected as Hindi
    school_ids = fields.Many2one('school.school2', string="School", domain='[("medium_ids.name", "=", medium)]',
                                 tracking=True)  # Giving Domain To school id
    principal_name = fields.Char(string='Principal Name', related='school_ids.employee_ids.name',
                                 tracking=True)  # using related field for school principal post
    total_fees = fields.Char(string="School Fees", compute="_compute_total_fees_of_school",
                             tracking=True)  # Computing Fees
    due_fees = fields.Char(string="Due Fees", compute="_compute_fees_to_pay", store=True)  # Compute Due fees
    hobby_ids = fields.Many2many('school.student.hobby', string="Hobby",
                                 tracking=True)  # Many2many relationship can select more then one hobby
    mobile = fields.Char(string="Mobile", help="Mobile number of the student", tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'Payment Processing'), ('Done', 'Done'), ('Failed', 'Payment Failed')],
        string="Payment Status")



    # @property
    # def _sequence_monthly_regex(self):
    #     return self.journal_id.sequence_override_regex or super()._sequence_monthly_regex
    #
    # @property
    # def _sequence_yearly_regex(self):
    #     return self.journal_id.sequence_override_regex or super()._sequence_yearly_regex
    #
    # @property
    # def _sequence_fixed_regex(self):
    #     return self.journal_id.sequence_override_regex or super()._sequence_fixed_regex

    def action_copy_phone_to_mobile(self):
        """
        This method copies the phone number to the mobile number field
        of the student record if it doesn't already exist.
        """
        for record in self:
            if record.phone and not record.mobile:  # Check if phone exists and mobile is empty
                record.write({'mobile': record.phone})  # Copy phone to mobile
                _logger.info(f"Copied phone number {record.phone} to mobile for student {record.name}")

    # =====================
    # Adding Validation for entering new Enrollment Number
    # =====================

    # @api.constrains ('en_number')
    # def _find_student_enrollment (self) :
    #     data = self.env['school.student'].search ([('en_number', '=', self.en_number), ('id', '!=', self.id)])  # excluded current id so it won't be getting current data id.
    #     if data :  # if any data is received function will throw error
    #         raise ValidationError (
    #             f"Error {data.mapped ('en_number')} \n Name {data.mapped ('name')}")  # Using mapped function to reduce code

    # =====================
    # Simple Phone Validation
    # =====================

    @api.constrains('phone')
    def _check_phone_number(self):
        filtered_phone = ''.join(filter(str.isdigit, self.phone))

        if len(filtered_phone) != 10 and filtered_phone[0] not in '123456789':
            raise ValidationError(
                f"Invalid Contact Number: {self.phone} \n Entered {len(filtered_phone)} Digits, And Numbers Only Required.")

    # @api.constrains ('amount_paid')
    # def _check_amount_paid (self) :
    #     for record in self :
    #         if record.amount_paid <= 0 :
    #             raise ValidationError ("Amount Paid must be greater than zero.")

    # =====================
    # Simple Print Function
    # =====================

    def school_demo(self):
        print(self, "This is simple function trying to run inside School Students Model")

    # No more applicable in odoo 17
    # ====================
    # name_get() Function
    # ====================

    # @api.onchange ('name')
    # def name_get (self) :
    #     result = []
    #     data = self.env['school.student'].search ([])
    #     for record in data :
    #         name = record.name  # Or whatever field you want to display
    #         result.append ((record.id, name))
    #     for i in result :
    #         print (i[1])

    # ====================
    # Giving Validation For Phone Number
    # ====================

    @api.model
    def create(self, vals):
        _logger.info("Appointment Has Been Booked _____________________: %s", vals)

        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('en.number')

        print(vals.get('reference'))

        return super().create(vals)

    # ====================
    # Search, search_read, read_group Methods
    # ====================

    @api.onchange('name')
    def _change_vals(self):
        all_rec = self.env['school.student'].search([('medium', '=', 'English')])  # Search FUnction

        al_rec_vals = self.env['school.student'].search_read([('medium', '=', 'English')])  # search_read function

        for i in all_rec:
            print("Records From Search Method Are called by obj.column_name : ", i.name)  # accessing object data
            print(" \n")

        for i in al_rec_vals:
            print("Records From search_read Are called by dictionary value object['col_names'] : ",
                  i['name'])  # accessing dictionary value
            print(" \n")

        # ====================
        # read_group returns JSON formate of data
        # ====================

        rec = self.env['school.student'].read_group([], fields=['school_ids'],  # which fields should be grouped
                                                    groupby=['school_ids'])  # adding domain and group by from function
        count = 0
        print(rec)
        for i in rec:
            print(i)
            count += i['school_ids_count']
            if i['school_ids']:
                school_id, school_name = i[
                    'school_ids']  # we receive a tuple as ids and assign this values to two variables
                print(f"School: {school_name} has {i['school_ids_count']} Students")
                print(" \n")
            else:
                print("No school associated.")
        print("Total Students Are : ", count)
        print(" \n")

    # ====================
    # Write Function Called When Updated
    # ====================

    def write(self, vals):
        rec = super(Students, self).write(vals)
        _logger.info("Students Info Updated : %s", vals)  # It will display updated values in log info
        print("________________________", rec)
        return rec

    # ====================
    # Search Operation
    # ====================

    def _search_student_by_age(self, operator, value):
        return [('age', operator,
                 value)]  # by default search is saved inside database so this will not work until it is called it will return proper result

    # ====================
    # Compute Function for fees
    # ====================

    @api.depends('total_fees', 'school_ids', 'due_fees', 'amount_paid')
    def _compute_total_fees_of_school(self):
        for rec in self:
            if rec.school_ids:
                rec.total_fees = rec.school_ids.fees_amount  # fetching total amount from school table
                if rec.amount_paid <= rec.school_ids.fees_amount:  # comparing values inserted and actual value
                    rec.due_fees = rec.school_ids.fees_amount - rec.amount_paid
                else:
                    rec.due_fees = "Invalid Amount"
            else:
                rec.total_fees = 0.0

    # ====================
    # Compute Age From Birth Date
    # ====================

    @api.depends('birth_date')
    def _compute_age_from_date(self):
        for rec in self:
            if rec.birth_date:
                birth_date = fields.Date.from_string(rec.birth_date)
                today = date.today()  # current date
                age = today.year - birth_date.year
                rec.age = age  # finding birthdate from selected date
            else:
                rec.age = 00

    # ====================
    # Updating Fees By Selecting School
    # ====================

    @api.depends('due_fees')
    def _compute_fees_to_pay(self):
        for rec in self:
            rec.due_fees = 0.0  # default value will be 0.0 for due fees until you select school

    # ====================
    # Find Schools from medium
    # ====================

    @api.onchange('medium')
    def _onchange_medium(self):
        if self.medium:
            # Search for schools with the selected medium
            schools = self.env['school.school2'].search([('medium_ids.name', '=',
                                                          self.medium)])  # if medium is selected it's school will be displayed according to domain we declare
            school_names = [f'{ school.name } / { school.email }' for school in
                            schools]  # school names related to the selected medium will be stored in this list

            _logger.info("Schools with medium '%s': %s", self.medium, school_names)

    # ====================
    # On Delete Some Info will be logged in terminal
    # ====================


    def unlink(self):
        result = super(Students, self).unlink()
        _logger.info("Unlinking == ========= %s", result)  # log will display true or false as value is deleted
        return result

    def action_cancel(self):
        self.write({'state' : 'Failed'})
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
        self.write({'state' : 'in_progress'})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params':
                {
                    'title': 'Payment Registered',
                    'message': 'Payment has been added for review!',
                    'sticky': False,
                    'type': 'info',
                }}

    def action_confirm(self):
        self.write({'state': 'Done'})
        return {'effect': {'fadeout': 'slow', 'message': 'Payment Is Successful', 'type': 'rainbow_man', }}


class Hobby(models.Model):
    _name = 'school.student.hobby'
    _description = 'hobby of students'

    name = fields.Char(string="Name")

# -c odoo.conf -d odoo17_owl
