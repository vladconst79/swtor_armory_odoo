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


    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
