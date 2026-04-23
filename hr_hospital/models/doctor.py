from odoo import fields, models


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _discription = 'Hospital Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Specialization')
