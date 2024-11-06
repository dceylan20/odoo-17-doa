# -*- coding: utf-8 -*-
{
    'name': "supplierClassification",

    'summary': "All Development about supplier classification on contacts",

    'description': """
Module to classify suppliers
    """,

    'author': "Doğa Ceylan",
    'website': "https://steelify.com", 
    'category': 'Contacts',
    'version': '17.1.0',
    'depends': ['base', 'contacts', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/editing.xml',
        'views/supplier_classification_view.xml',       
    ],

   

    'installable': True,
    'auto_install': False,
}

