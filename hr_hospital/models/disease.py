from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    """Disease classifier with parent/child hierarchy.

    Uses ``_parent_store`` for efficient hierarchical queries. The
    ``complete_name`` shows the full path (e.g. "Respiratory / Flu").
    """

    _name = 'hr.hospital.disease'
    _description = 'Disease Type'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'name'

    name = fields.Char(string='Disease Name', required=True, translate=True)
    parent_id = fields.Many2one(
        'hr.hospital.disease',
        string='Parent disease',
        ondelete='set null',
        index=True,
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        'hr.hospital.disease',
        'parent_id',
        string='Sub-diseases',
    )
    complete_name = fields.Char(
        string='Full Name',
        compute='_compute_complete_name',
        recursive=True,
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for rec in self:
            if rec.parent_id:
                rec.complete_name = f'{rec.parent_id.complete_name} / {rec.name}'
            else:
                rec.complete_name = rec.name or ''

    @api.depends('complete_name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.complete_name or rec.name or ''

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if self._has_cycle():
            raise ValidationError(
                'You cannot create a recursive disease hierarchy.'
            )
