from datetime import date

from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    """Abstract medical info — mixed into doctor and patient models.

    Provides blood type, gender, birthday and a computed age.
    """

    _name = 'hr.hospital.medic.info'
    _description = 'Hospital medical information (abstract)'

    blood_type = fields.Selection(
        selection=[
            ('o_plus', 'O(I) Rh+'),
            ('o_minus', 'O(I) Rh-'),
            ('a_plus', 'A(II) Rh+'),
            ('a_minus', 'A(II) Rh-'),
            ('b_plus', 'B(III) Rh+'),
            ('b_minus', 'B(III) Rh-'),
            ('ab_plus', 'AB(IV) Rh+'),
            ('ab_minus', 'AB(IV) Rh-'),
        ],
        string='Blood Type',
    )
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')],
        string='Gender',
    )
    birthday = fields.Date(string='Date of Birth')
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
    )

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birthday:
                bd = rec.birthday
                rec.age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            else:
                rec.age = 0
