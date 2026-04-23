from odoo import fields, models


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _discription = 'Patient visit'

    date = fields.Datetime(string='Visit Date', default=fields.Datetime.now)
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hr.hospital.patient', string='Patient', required=True)
    disease_id = fields.Many2one('hr.hospital.disease', string='Diagnoses')
