{
    'name': 'Invoice PDF Report',
    'version': '1.0',
    'sequence': -1,
    'category': 'Accounting',
    'summary': 'Generate PDF Reports for Factures (Invoices)',
    'author': 'Your Name',
    'license': 'LGPL-3',  # Added license key to remove warning
    'depends': ['account', 'sale', 'stock', 'sale_management','invoice_report'],
    'data': [
        'security/ir.model.access.csv',
        'views/facture_proforma_new_menu.xml',
        # 'reports/facture_report_template.xml',
        # 'reports/sale_order_custom_report.xml',
        # 'reports/delivery_report.xml',
        # 'reports/return_report.xml',
        'reports/withholding_certificate_tax.xml',
        'views/report_view.xml',
        'views/product_description.xml',
        'views/sale_order_quotation_remove_pdf.xml',
        'data/invoice_sequence.xml',
        # 'views/view_picking_form_custom.xml',
        'views/view_facture.xml',
    ],
    'installable': True,
    'application': True,
}

