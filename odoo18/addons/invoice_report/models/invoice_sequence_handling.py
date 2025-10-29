from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        for rec in res:
            name = self.env['ir.sequence'].next_by_code(
                'account.invoice.proforma')
            rec.name = name
        return res
    def action_generate_report_fr_facture(self):
        # Trigger the report generation for this project
        report_action = self.env.ref('invoice_report_custom.action_invoice_report')
        return report_action.report_action(self)
 