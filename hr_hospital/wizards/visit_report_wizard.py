from odoo import api, fields, models


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Visit report wizard'

    doctor_ids = fields.Many2many(
        'hr.hospital.doctor',
        'visit_report_wizard_doctor_rel',
        'wizard_id',
        'doctor_id',
        string='Doctors',
    )
    patient_ids = fields.Many2many(
        'hr.hospital.patient',
        'visit_report_wizard_patient_rel',
        'wizard_id',
        'patient_id',
        string='Patients',
    )
    date_from = fields.Date(string='Period start')
    date_to = fields.Date(string='Period end')
    only_done = fields.Boolean(string='Only completed visits')
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []
        active_id = self.env.context.get('active_id')
        if not active_ids and active_id:
            active_ids = [active_id]
        if active_model == 'hr.hospital.doctor' and active_ids:
            res['doctor_ids'] = [(6, 0, active_ids)]
        elif active_model == 'hr.hospital.patient' and active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]
        return res

    def action_show_visits(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.date_from:
            domain.append(('scheduled_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_date', '<=', self.date_to))
        if self.only_done:
            domain.append(('state', '=', 'done'))
        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))
        list_view = self.env.ref('hr_hospital.view_visit_tree', raise_if_not_found=False)
        form_view = self.env.ref('hr_hospital.view_visit_form', raise_if_not_found=False)
        views = []
        if list_view:
            views.append((list_view.id, 'list'))
        else:
            views.append((False, 'list'))
        if form_view:
            views.append((form_view.id, 'form'))
        else:
            views.append((False, 'form'))
        return {
            'name': 'Visits',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'views': views,
            'domain': domain,
            'target': 'main',
        }
