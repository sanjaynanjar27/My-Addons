# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': "My Todo App",
    'version': '17.0.0.1',
    'license': 'OPL-1',
    'summary': """MY Todo App""",
    'category': 'sale',
    'description': """
        Create a Todo List
    """,
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'https://www.caretit.com',
    'depends': ['base','contacts','web','website'],
    'data': [
        'views/template.xml',
    ],
    "assets": {
        "web.assets_frontend": [
            "my_todo_app/static/src/my_app.js",
            "/my_todo_app/static/src/js/todo_list.js",
            "/my_todo_app/static/src/js/todo_item.js",
        ],
        "web.assets_qweb": [
            "/my_todo_app/static/src/xml/todo_item_view.xml",
            "/my_todo_app/static/src/xml/todo_list_view.xml"
        ],
    },
    'images': [],
    'price': 99.00,
    'currency': 'EUR',
}
