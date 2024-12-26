# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': "User Login/Logout Status",
    'summary': """""",
    'description': """
        User Login/Logout Status and User total Login Time Status viewer
    """,
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'https://www.caretit.com',
    'category': 'Administration',
    'version': '17.0',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/setting.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'cit_user_login_status/static/src/js/SessionExpiredCustomDialog.js',
            # 'cit_user_login_status/static/src/xml/session_expired_custom_dialog.xml',
            'cit_user_login_status/static/src/xml/custom_session_expired_template.xml',
        ],
    },
    'license': 'AGPL-3',
}
