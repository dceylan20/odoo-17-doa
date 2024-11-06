# -*- coding: utf-8 -*-
{
    'name': "inventoryCoating",

    'summary': "All Development about coating on inventory",

    'description': """
Module to change fields of coating from selection to many2one
    """,

    'author': "Doğa Ceylan",
    'website': "https://yenaengineering.nl", 
    'category': 'Inventory',
    'version': '17.1.0',
    'depends': ['base', 'product'],

    'data': [
        'views/coating_view.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'auto_install': False,
}

