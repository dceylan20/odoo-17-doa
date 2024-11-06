{
    'name': 'Batch Transfer',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Extends Batch Transfer with additional fields',
    'author': 'Emre Mataracı, Doğa Ceylan',
    'website': 'http://yenaengineering.nl',
    'depends': ['stock', 'project', 'purchase', 'contacts'],
    'data': [
        'views/batch_transfer_view.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml'
    ],
    'installable': True,
    'auto_install': False,
}