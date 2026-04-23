from odoo import fields, models


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _discription = 'Disease Type'

    name = fields.Char(string='Disease Name', required=True)
