from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


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
    same_disease_visit_count = fields.Integer(
        string='Visits with same disease',
        compute='_compute_same_disease_visit_count',
    )
    visit_month = fields.Char(
        string='Visit month',
        compute='_compute_visit_month',
        store=True,
    )

    @api.depends('disease_id')
    def _compute_same_disease_visit_count(self):
        for rec in self:
            if rec.disease_id:
                rec.same_disease_visit_count = self.search_count(
                    [('disease_id', '=', rec.disease_id.id)]
                )
            else:
                rec.same_disease_visit_count = 0

    @api.depends('scheduled_date')
    def _compute_visit_month(self):
        for rec in self:
            if rec.scheduled_date:
                rec.visit_month = fields.Datetime.to_datetime(
                    rec.scheduled_date
                ).strftime('%Y-%m')
            else:
                rec.visit_month = ''

    def action_open_same_disease_visits(self):
        self.ensure_one()
        if not self.disease_id:
            return False
        return {
            'name': 'Visits with the same disease',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('disease_id', '=', self.disease_id.id)],
            'context': {'default_disease_id': self.disease_id.id},
        }

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

    def _is_install_context(self):
        ctx = self.env.context
        return bool(ctx.get('install_mode') or ctx.get('install_demo') or ctx.get('module'))

    @api.constrains('scheduled_date', 'doctor_id')
    def _check_completed_visit_immutable(self):
        for rec in self:
            if self._is_install_context():
                continue
            # create_date != write_date means the record was modified
            # after its creation -- i.e. this is an edit, not a creation.
            if (rec.state == 'done' and rec.create_date and rec.write_date
                    and rec.create_date != rec.write_date):
                raise ValidationError(
                    'You cannot change date/time or doctor '
                    'of a completed visit.'
                )

    def action_archive(self):
        if not self._is_install_context():
            for rec in self:
                if rec.state == 'done':
                    raise UserError('You cannot archive a completed visit.')
        return super().action_archive()

    def action_unarchive(self):
        return super().action_unarchive()

    def unlink(self):
        if not self._is_install_context():
            for rec in self:
                if rec.state == 'done':
                    raise UserError('You cannot delete a completed visit.')
        return super().unlink()

    def action_mark_done(self):
        for rec in self:
            rec.write({
                'state': 'done',
                'visit_date': rec.visit_date or fields.Datetime.now(),
            })
        return True

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        return True

    def action_reset_to_planned(self):
        self.write({'state': 'planned'})
        return True
