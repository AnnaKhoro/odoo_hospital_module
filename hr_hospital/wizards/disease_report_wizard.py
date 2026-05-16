from odoo import api, fields, models


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Monthly disease report wizard'

    doctor_ids = fields.Many2many(
        'hr.hospital.doctor',
        'disease_report_wizard_doctor_rel',
        'wizard_id', 'doctor_id',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        'hr.hospital.disease',
        'disease_report_wizard_disease_rel',
        'wizard_id', 'disease_id',
        string='Diseases',
    )
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

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
        today = fields.Date.context_today(self)
        first = today.replace(day=1)
        if today.month == 12:
            next_first = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_first = today.replace(month=today.month + 1, day=1)
        from datetime import timedelta
        last = next_first - timedelta(days=1)
        res.setdefault('date_from', first)
        res.setdefault('date_to', last)
        return res

    def action_generate(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        if self.date_from:
            domain.append(('scheduled_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_date', '<=', self.date_to))
        return {
            'name': 'Visits by disease',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar,pivot,graph',
            'domain': domain,
            'context': {'search_default_group_disease': 1},
            'target': 'main',
        }
