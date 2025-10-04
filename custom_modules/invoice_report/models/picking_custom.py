from odoo import fields, models , api

class PickingCustom(models.Model):
    _inherit = 'stock.picking'

    def action_generate_report_bon_de_livraison(self):
        # Trigger the report generation for this project
        report_action = self.env.ref('invoice_report.invoice_report_template')
        return report_action.report_action(self)