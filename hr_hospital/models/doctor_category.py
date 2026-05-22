from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Doctor Qualification Category'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, translate=True)
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
