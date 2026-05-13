from odoo import api, fields, models
from odoo.exceptions import UserError


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'scheduled_date desc, id desc'

    name = fields.Char(string='Reference', compute='_compute_name', store=True)
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='planned',
        required=True,
    )
    scheduled_date = fields.Datetime(
        string='Scheduled date',
        required=True,
        default=fields.Datetime.now,
    )
    visit_date = fields.Datetime(string='Actual visit date')
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True,
    )
    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Disease',
    )
    summary = fields.Html(string='Summary / Epicrisis')
    active = fields.Boolean(default=True)

    @api.depends('patient_id', 'doctor_id', 'scheduled_date')
    def _compute_name(self):
        for rec in self:
            parts = [
                rec.patient_id.name or '',
                rec.doctor_id.name or '',
            ]
            if rec.scheduled_date:
                parts.append(fields.Datetime.to_string(rec.scheduled_date))
            rec.name = ' / '.join(p for p in parts if p)

    _PROTECTED_FIELDS = ('scheduled_date', 'visit_date', 'doctor_id')

    def _is_install_context(self):
        ctx = self.env.context
        return bool(ctx.get('install_mode') or ctx.get('install_demo') or ctx.get('module'))

    def write(self, vals):
        if not self._is_install_context():
            for rec in self:
                if rec.state == 'done' and any(f in vals for f in self._PROTECTED_FIELDS):
                    raise UserError('You cannot change date/time or doctor of a completed visit.')
                if rec.state == 'done' and vals.get('active') is False:
                    raise UserError('You cannot archive a completed visit.')
        return super().write(vals)

    def unlink(self):
        if not self._is_install_context():
            for rec in self:
                if rec.state == 'done':
                    raise UserError('You cannot delete a completed visit.')
        return super().unlink()
