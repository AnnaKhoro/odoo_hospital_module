{
    'name': 'Hospital Management',
    'summary': 'Module for hospital automation: doctors and patients',
    'author': 'Anna Khoroshylova',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'version': '19.0.1.3.0',

    'depends': [
        'base',
        'web',
    ],

    'data': [
        'security/ir.model.access.csv',

        'data/doctor_category_data.xml',
        'data/disease_data.xml',

        'views/doctor_category_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/doctor_history_views.xml',

        'wizards/mass_reassign_doctor_wizard_views.xml',
        'wizards/visit_report_wizard_views.xml',
        'wizards/disease_report_wizard_views.xml',

        'reports/doctor_report.xml',
        'reports/doctor_report_template.xml',

        'views/menu_views.xml',
    ],

    'demo': [
        'demo/disease_demo.xml',
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/doctor_history_demo.xml',
        'demo/visit_demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png',
    ],
}
