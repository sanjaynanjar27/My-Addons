# -*- coding: utf-8 -*-
{
    'name':        'Owl Tutorial',
    'version':     '1.0',
    'summary':     'OWL Tutorial',
    'sequence':    -1,
    'license': 'LGPL-3',
    'description': """OWL Tutorial Custom Dashboard""",
    'category':    'OWL',
    'depends':     ['base', 'web', 'sale', 'board', 'custom_employee'],
    'data':        [
        'views/sales_dashboard.xml',
    ],
    'demo':        [
    ],
    'installable': True,
    'application': True,
    'assets':      {
        'web.assets_backend': [
            'owl/static/src/components/sale_dashboard.js',
            'owl/static/src/components/sale_dashboard.xml',
            'owl/static/src/components/chart_renderer/chart_renderer.js',
            'owl/static/src/components/chart_renderer/chart_renderer.xml',
            'owl/static/src/components/kpi_card/kpi_card.js',
            'owl/static/src/components/kpi_card/kpi_card.xml',
            'owl/static/src/components/moment.min.js',
            'owl/static/src/components/valid_email_field/valid_email_field.js',
            'owl/static/src/components/valid_email_field/valid_email_field.xml',
            'owl/static/src/components/copy_to_clipboard_widget/copy_to_clipboard.js',
            'owl/static/src/components/copy_to_clipboard_widget/copy_to_clipboard.xml',
            'owl/static/src/components/copy_to_clipboard_widget/copy_to_clipboard.css',
            'owl/static/src/css/dashboard.css',
        ],
    },
}
