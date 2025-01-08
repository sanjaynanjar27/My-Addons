from odoo import api, models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    """
        The condition uses a POSIX regular expression (~*) to validate the email format:
        ~* is case-insensitive matching.
        The regex '^[^@\s]+@[^@\s]+\.[^@\s]+$' ensures that:
        The email has characters before and after the @ symbol.
        There is at least one dot (.) after the @ symbol.
    """

    restrict_mail = fields.Boolean(string='Restrict Mail?', default=False,
                                   help="If True Mails Will be restricted for Partner and won't be able to receive Alerts Or Mails.")
    credit_limit = fields.Float(string="User Credit Limit", required=True)

    _sql_constraints = [
        ('email_validation',
         "CHECK (email ~* '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$')",
         'Email address is invalid.'),
        ('email_repeated',
         'UNIQUE(email)',
         'Email address is already been used.'),
    ]

    @api.constrains('credit_limit')
    def validate_credit_limit(self):
        for record in self:
            if record.credit_limit < 0:
                raise models.ValidationError("Credit Limit cannot be negative.")
