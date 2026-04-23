{
    'name': 'Hospital Management',
    'summary': 'Module for hospital automation: doctors and patients',
    'author': 'Anna Khoroshylova',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'version': '19.0.1.0.0',

    'depends': [
        'base',
    ],


    'data': [
        'security/ir.model.access.csv',
        'data/disease_data.xml',

        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/menu_views.xml',
    ],

    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}