    # -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
{
    'name': 'Custom Session',
    'description': """
    Custom Session Destroyer
    ========================
    If you want to add customized session logout feature this will add new field to your account and it will expire your session after chosen countdown

    Features : 
    - Adds New Field To Database And Input to your User profile 
    - At a specific count down it will destroy users session   
    """,
    'license': 'LGPL-3',
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'https://www.caretit.com',
    'category': 'Administration',
    'version': '17.0',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_user_custom_field.xml',
        'views/res_devices_view.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'custom_session/static/src/js/count_down.js',
            'custom_session/static/src/js/template_logout.js',
            'custom_session/static/src/xml/count_down.xml',
        ],
    },
}
