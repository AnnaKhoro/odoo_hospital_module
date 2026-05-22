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
    phone = fields.Char(string='Phone')
    user_id = fields.Many2one(
        'res.users', string='System User',
        help='Linked portal user (used for security record rules).',
    )
    visit_ids = fields.One2many(
        'hr.hospital.visit', 'patient_id', string='Visit history',
    )
    visit_count = fields.Integer(
        string='Visits count', compute='_compute_visit_count',
    )

    def _compute_visit_count(self):
        for rec in self:
            rec.visit_count = len(rec.visit_ids)

    def action_open_visits(self):
        self.ensure_one()
        return {
            'name': 'Visits',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_new_visit(self):
        self.ensure_one()
        return {
            'name': 'New visit',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

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
