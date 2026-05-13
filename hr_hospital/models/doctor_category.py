from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Doctor Qualification Category'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    doctor_ids = fields.One2many(
        'hr.hospital.doctor',
        'category_id',
        string='Doctors',
    )

    _name_uniq = models.Constraint(
        'unique(name)',
        'A category with this name already exists.',
    )

    @api.constrains('name')
    def _check_name_unique(self):
        for rec in self:
            name = (rec.name or '').strip().lower()
            if not name:
                continue
            duplicate = self.search(
                [
                    ('id', '!=', rec.id),
                    ('name', '=ilike', name),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError('A category with this name already exists.')
