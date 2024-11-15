{
    'name': "YENA Contact Development",
    'version': '15.1.0',
    'summary': "All Development about res.partner",
    'author': "Alperen Alihan ER, Doğa Ceylan",
    'website': "https://yenaengineering.nl",
    'category': 'Contact',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'contacts', 'contact_status'],
    'data': [
        'views/contact_development.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}