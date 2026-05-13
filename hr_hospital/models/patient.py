from odoo import fields, models


class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Hospital Patient'

    name = fields.Char(string='Full Name', required=True)
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Personal doctor',
    )
    doctor_history_ids = fields.One2many(
        'hr.hospital.doctor.history',
        'patient_id',
        string='Personal doctor history',
    )
    insurance_policy_number = fields.Char(
        string='Insurance policy number',
        size=20,
    )

    def write(self, vals):
        track = 'doctor_id' in vals and not self.env.context.get('skip_doctor_history')
        if track:
            today = fields.Date.context_today(self)
            new_doctor = vals.get('doctor_id')
            for rec in self:
                old_doctor = rec.doctor_id.id
                if new_doctor != old_doctor:
                    active_history = rec.doctor_history_ids.filtered(lambda h: h.active and not h.change_date)
                    active_history.write({'change_date': today})
                    if new_doctor:
                        self.env['hr.hospital.doctor.history'].create(
                            {
                                'patient_id': rec.id,
                                'doctor_id': new_doctor,
                                'assignment_date': today,
                            }
                        )
        return super().write(vals)
