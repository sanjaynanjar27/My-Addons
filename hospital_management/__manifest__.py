{
    'name': 'Hospital Management',
    'author': 'Caret IT Solutions',
    'version': '1.0',
    'license': 'LGPL-3',
    # Specify the license here
    'depends': ['mail', 'board', 'website', ],

    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'views/doctor_view.xml',
        'views/new_appointment_wizard.xml',
        'reports/hospital_doctor_report.xml',
        'reports/hospital_doctor_template.xml',
        'reports/report.xml',
        'reports/report_template.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view_only.xml',
        'views/hospital_management_wizard_view.xml',
        'views/menu.xml',
        'data/patient_sequance.xml',
        'data/appointment_seq.xml',
        'views/doctor_controller_view.xml',
        'views/extend_cid.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'hospital_management/static/src/css/custom_radio.css',
        ],
    },
    'application': True,
}
