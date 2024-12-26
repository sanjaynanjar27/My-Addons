{
    'name': 'Library Management System',
    'version': '1.0',
    'summary': 'Module to handle library management',
    'sequence': 10,
    'description': """
Library Management System
=========================
This module allows the management of books, members, and borrowing processes in a library. It provides an easy-to-use interface for tracking library inventory, managing book checkouts and returns, and keeping member records.

It is designed to help libraries manage their day-to-day operations in a more efficient and organized manner.
    """,
    'category': 'Services/Library',
    'website': 'https://www.caretitsolutions.com',
    'depends': ['base', 'mail'],  # Add any relevant dependencies here
    'data': [
        'security/ir.model.access.csv',
        'views/books_view.xml',
        'views/menu.xml',
        'reoprt/report_template.xml',
        'views/template_view.xml',
        'views/form_template.xml',
        'views/success_page_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
