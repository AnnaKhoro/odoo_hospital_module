from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Hospital Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Specialization')
    category_id = fields.Many2one(
        'hr.hospital.doctor.category',
        string='Category',
    )
    user_id = fields.Many2one('res.users', string='System User')
    is_intern = fields.Boolean(
        string='Is intern',
        compute='_compute_is_intern',
        store=True,
    )
    mentor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Mentor',
        domain="[('is_intern', '=', False)]",
    )
    mentee_ids = fields.One2many(
        'hr.hospital.doctor', 'mentor_id', string='Interns (mentees)',
    )
    mentee_names = fields.Char(
        string='Interns list',
        compute='_compute_mentee_names',
    )

    @api.depends('mentee_ids', 'mentee_ids.name')
    def _compute_mentee_names(self):
        for rec in self:
            rec.mentee_names = ', '.join(rec.mentee_ids.mapped('name'))
    color = fields.Integer(string='Color Index', default=0)
    patient_ids = fields.One2many(
        'hr.hospital.patient', 'doctor_id', string='Patients',
    )
    visit_count = fields.Integer(
        string='Visits', compute='_compute_visit_count',
    )

    def _compute_visit_count(self):
        for rec in self:
            rec.visit_count = self.env['hr.hospital.visit'].search_count(
                [('doctor_id', '=', rec.id)]
            )

    def action_open_visits(self):
        self.ensure_one()
        return {
            'name': 'Visits',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
        }

    _INTERN_KEYWORDS = ('інтерн', 'intern')

    @api.depends('category_id', 'category_id.name')
    def _compute_is_intern(self):
        for rec in self:
            name = (rec.category_id.name or '').lower() if rec.category_id else ''
            rec.is_intern = any(kw in name for kw in self._INTERN_KEYWORDS)

    @api.constrains('mentor_id', 'is_intern', 'category_id')
    def _check_mentor_not_intern(self):
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError('An intern cannot be selected as a mentor.')
            if rec.is_intern:
                mentees = self.search(
                    [
                        ('mentor_id', '=', rec.id),
                    ]
                )
                if mentees:
                    raise ValidationError(
                        "Doctor '%s' is a mentor for: %s. "
                        'Reassign them before changing this doctor '
                        'to intern category.' % (rec.name, ', '.join(mentees.mapped('name')))
                    )
