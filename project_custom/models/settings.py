from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    global_credit_limit = fields.Float(
        string='Global Credit Limit',
        help='Set a global credit limit for all partners.'
    )

    @api.constrains('global_credit_limit')
    def valid_credit_limit(self):
        for record in self:
            if record.global_credit_limit < 0:
                raise models.ValidationError("Credit Limit cannot be negative.")

    @api.model
    def get_values(self):
        """
        Load the global credit limit value from the ir.config_parameter.
        """
        res = super(ResConfigSettings, self).get_values()
        icp = self.env['ir.config_parameter'].sudo()
        res.update(
            global_credit_limit=float(icp.get_param('res.config.global_credit_limit', default=0.0))
        )
        print(f"\n================================{res}")

        i_want = float(icp.get_param('res.config.global_credit_limit'))

        print(f"\nI Want: {i_want}")
        return res

    def set_values(self):
        """
        Store the global credit limit value to the ir.config_parameter.
        """
        super(ResConfigSettings, self).set_values()
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('res.config.global_credit_limit', self.global_credit_limit)