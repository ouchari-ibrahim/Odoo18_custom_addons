from odoo import models, api
from num2words import num2words

class CustomInvoiceReport(models.AbstractModel):
    _name = 'report.invoice_report_custom.invoice_report_custom_template'
    _description = 'Custom Invoice Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        return {
            'doc': docs,  # This is crucial: ensure 'doc' is correctly passed to the template
            'doc_ids': docids,
            'doc_model': 'account.move',
        }

    def convert_amount_to_words(amount, lang='fr'):
        return num2words(amount, lang=lang)