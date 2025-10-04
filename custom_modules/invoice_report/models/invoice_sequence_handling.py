from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals_list):
        # Allow batch creation
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        records = super(AccountInvoice, self).create(vals_list)

        for rec in records:
            if rec.move_type in ('out_invoice', 'out_refund', 'out_receipt'):  # only for invoices
                name = self.env['ir.sequence'].next_by_code('account.invoice.proforma') or '/'
                rec.name = name
        return records

    def action_generate_report_fr_facture(self):
        # Trigger the report generation for this invoice
        report_action = self.env.ref('invoice_report.action_invoice_report')
        return report_action.report_action(self)
