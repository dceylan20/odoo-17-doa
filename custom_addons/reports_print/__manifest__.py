{
    'name': 'Reports Print',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Custom reports for Odoo',
    'description': """
    Reports Print
    ============
    This module provides custom print reports for various Odoo models.
    """,
    'author': 'Emre MATARACI, Doğa CEYLAN',
    'website': 'https://www.yenaengineering.nl',
    'depends': ['base', 'purchase'],
    'data': [
        'reports/report_purchase_print.xml',
        'reports/report_template_purchase_print.xml',
        'reports/reports_print.external_layout_yena.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
