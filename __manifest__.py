# -*- coding: utf-8 -*-
{
    'name': "SWTOR Armory",

    'summary': """
        A module to manage your SWTOR character.
        """,

    'description': """
        A module to manage your SWTOR character.
    """,

    'author': "Greuceanu",
    'website': "",

    'category': 'Uncategorized',
    'version': '16.0.0.0.1',


    'depends': [
        'base',
        'web',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/crew_skill_wizard.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/character_views.xml',
        'views/crew_skill_views.xml',
        'views/operation_views.xml',
        'views/class_name_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # '/swtor_armory/static/src/js/class_name_widget.js',
        ],
        'web.assets_backend_prod_only': [
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
}
