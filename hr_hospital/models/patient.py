from odoo import fields, models


class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _discription = 'Hospital patient'

    name = fields.Char(string='Full Name', required=True)
    birthday = fields.Date(string='Date of Birth')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Personal doctor')
