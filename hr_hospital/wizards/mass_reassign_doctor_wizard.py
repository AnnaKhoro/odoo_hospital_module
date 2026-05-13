from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass reassign personal doctor'

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='New doctor',
        required=True,
    )
    change_date = fields.Date(
        string='Change date',
        default=fields.Date.context_today,
    )

    def action_apply(self):
        self.ensure_one()
        patient_ids = self.env.context.get('active_ids') or []
        if not patient_ids:
            return {'type': 'ir.actions.act_window_close'}
        patients = self.env['hr.hospital.patient'].browse(patient_ids)
        History = self.env['hr.hospital.doctor.history']
        for patient in patients:
            if patient.doctor_id.id == self.doctor_id.id:
                continue
            active_history = patient.doctor_history_ids.filtered(lambda h: h.active and not h.change_date)
            active_history.write({'change_date': self.change_date})
            History.create(
                {
                    'patient_id': patient.id,
                    'doctor_id': self.doctor_id.id,
                    'assignment_date': self.change_date,
                }
            )
            patient.with_context(skip_doctor_history=True).write({'doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
