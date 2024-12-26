{
    'name':        'School Management System',
    'version':     '1.0',
    'summary':     'Manage schools and their information',
    'sequence':    10,
    'description': """
School Management System
========================
This module provides functionalities to manage school information, including student records, employee details, school streams, and more. 
It helps educational institutions efficiently manage their daily operations, from student enrollments to staff management.

Key Features:
- Manage student and employee records
- Track school streams and classes
- Generate school-related reports
- Customizable school information management
    """,
    'category':    'Education',
    'website':     'https://www.yourschoolmanagement.com',
    'depends':     ['base', 'mail', 'board', 'website','product'],
    'data':        [
        'views/school_setting.xml',
        'data/sequence.xml',
        'views/streams_view.xml',
        'views/employee_view.xml',
        'views/student_view.xml',
        'views/school_view.xml',
        'reports/school_transiant_template.xml',
        'reports/school_transiant_report.xml',
        'reports/school_report.xml',
        'reports/school_template.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        'security/schools_access_group.xml',
        'reports/school_xlsx_reoprt.xml',
        'views/school_template.xml',
    ],
    'demo':        [
        'demo/school_student_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license':     'LGPL-3',
}
