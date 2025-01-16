{
    'name': 'OWL Task',
    'description': """
    OWL JS Task - [TO DO] List
    ========================
    To Do List Of Items using Owl functionalities

    Features : 
    - Adds New List Items 
    - Create more then one todo list   
    """,
    'license': 'LGPL-3',
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'https://www.caretit.com',
    'category': 'Tools',
    'version': '17.0',
    'depends': ['base', 'web'],
    'data': [
        'views/owl_list_of_to_do.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'owl_task/static/src/css/style.css',
            'owl_task/static/src/js/toDoTask.js',
            'owl_task/static/src/xml/my_list.xml',
        ],
    },
}
