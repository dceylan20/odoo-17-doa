{
    'name': 'YENA Sale Report',
    'version': '17.0',
    'category': 'Sale Report',
    'summary': 'Custom sale reports for Odoo',
    'description': """
    Reports Print
    ============
    This module provides custom print reports for various Odoo models.
    """,
    'website': 'https://www.yenaengineering.nl',
    'depends': ['base', 'purchase', 'yena_external_layout'],
    'data': [
        'reports/report_action.xml',
        'reports/report_sale_proposal_form.xml',
        ],

    'installable': True,
    'application': False,
    'auto_install': False,
}

