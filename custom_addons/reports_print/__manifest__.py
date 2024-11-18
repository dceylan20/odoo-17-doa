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
    'author': 'Emre MATARACI',
    'website': 'https://www.yenaengineering.nl',
    'depends': ['base', 'purchase'],
    'data': [
        'reports/sale/reports_print.external_layout_yena.xml',
        'reports/sale/reports_print.imzasız_external_layout_yena.xml',
    
        'reports/purchase/report_purchase_actions.xml',
        'reports/purchase/report_purchase_order.xml',
        'reports/purchase/report_purchase_order_cagri_mektubu.xml',
        'reports/purchase/report_purchase_rfq.xml',
        'reports/purchase/report_purchase_rfq_hedef.xml',
        ],

    'installable': True,
    'application': False,
    'auto_install': False,
}