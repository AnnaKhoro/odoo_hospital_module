from odoo import api, fields, models


class HospitalDoctorHistory(models.Model):
    _name = 'hr.hospital.doctor.history'
    _description = 'Personal Doctor History'
    _order = 'assignment_date desc, id desc'

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    assignment_date = fields.Date(
        string='Assignment date',
        required=True,
        default=fields.Date.context_today,
    )
    change_date = fields.Date(string='Change date')
    active = fields.Boolean(default=True)

    @api.onchange('assignment_date', 'change_date')
    def _onchange_change_date(self):
        for rec in self:
            if rec.assignment_date and rec.change_date and rec.change_date < rec.assignment_date:
                return {
                    'warning': {
                        'title': 'Invalid dates',
                        'message': ('Doctor change date cannot be earlier than the assignment date.'),
                    }
                }

    @api.depends('patient_id', 'doctor_id', 'doctor_id.category_id', 'assignment_date')
    def _compute_display_name(self):
        for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            category = rec.doctor_id.category_id.name if rec.doctor_id.category_id else ''
            assign = rec.assignment_date or ''
            rec.display_name = f'{patient} - {doctor} ({category}) {assign}'
