from datetime import date

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHospital(TransactionCase):
    """Cover key block-3 model methods of hr_hospital."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['hr.hospital.doctor.category']
        cls.Doctor = cls.env['hr.hospital.doctor']
        cls.Patient = cls.env['hr.hospital.patient']
        cls.Disease = cls.env['hr.hospital.disease']
        cls.History = cls.env['hr.hospital.doctor.history']

        cls.cat_intern = cls.Category.create({'name': 'TestIntern'})
        cls.cat_top = cls.Category.create({'name': 'TestTop'})

        cls.doctor_top = cls.Doctor.create({
            'name': 'Top Doctor',
            'specialization': 'Therapist',
            'category_id': cls.cat_top.id,
        })
        cls.doctor_intern = cls.Doctor.create({
            'name': 'Junior Intern',
            'specialization': 'Trainee',
            'category_id': cls.cat_intern.id,
            'mentor_id': cls.doctor_top.id,
        })
        cls.patient = cls.Patient.create({
            'name': 'John Test',
            'birthday': date(1990, 1, 1),
        })

    def test_doctor_category_sql_uniqueness(self):
        """SQL unique constraint blocks duplicate category names."""
        with self.assertRaises(Exception):
            with self.cr.savepoint():
                self.Category.create({'name': 'TestIntern'})

    def test_is_intern_computed(self):
        """is_intern is True for categories containing the 'intern' keyword."""
        self.assertTrue(self.doctor_intern.is_intern)
        self.assertFalse(self.doctor_top.is_intern)

    def test_mentor_cannot_be_intern(self):
        """ValidationError when the chosen mentor is an intern."""
        with self.assertRaises(ValidationError):
            self.doctor_intern.copy({
                'name': 'Other intern',
                'mentor_id': self.doctor_intern.id,
            })

    def test_doctor_history_display_name(self):
        """display_name follows '<patient> - <doctor> (<category>) <date>'."""
        history = self.History.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor_top.id,
            'assignment_date': date(2024, 1, 15),
        })
        self.assertIn('John Test', history.display_name)
        self.assertIn('Top Doctor', history.display_name)
        self.assertIn('TestTop', history.display_name)
        self.assertIn('2024-01-15', history.display_name)

    def test_disease_hierarchy_recursion(self):
        """Self-parenting in the disease hierarchy is blocked.

        Odoo's ``_parent_store_update`` may raise ``UserError`` before
        our ``_has_cycle`` check fires ``ValidationError`` — accept
        either.
        """
        d = self.Disease.create({'name': 'Root'})
        raised = False
        try:
            d.parent_id = d
        except (UserError, ValidationError):
            raised = True
        self.assertTrue(raised, 'Self-parenting should raise an error.')

    def test_patient_age_computed(self):
        """Age is computed from birthday."""
        today = date.today()
        expected = today.year - 1990 - (
            (today.month, today.day) < (1, 1)
        )
        self.assertEqual(self.patient.age, expected)
