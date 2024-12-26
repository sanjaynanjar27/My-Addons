{
    'name': 'Employee Data',
    'version': '1.0',
    'summary': 'Employee Details Management',
    'sequence': 10,
    'description': """
Employee Data Management
========================
This module provides functionalities to manage employee information. It includes features to store and display detailed employee records, generate employee reports, and manage employee documents. Ideal for organizations looking to keep track of their workforce information in an efficient and organized manner.

Key Features:
- Employee personal and job details
- Employee report generation
- Document management for employees
- Customizable employee record management
    """,
    'category': 'Tools',
    'website': 'https://www.caretitsolutions.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_view.xml',
        'wizard/employee_report_view.xml',
        'report/report.xml',
        'report/reoprt_employee_document.xml',
        'data/sequence.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
