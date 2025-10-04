from odoo import models, fields, api , _
from num2words import num2words
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    amount_total_text = fields.Char(string="Total Amount in Words", compute="_compute_amount_total_text")
    def action_view_all_move_lines(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_line_select').read()[0]
        action['domain'] = [('move_id', '=', self.id)]
        action['context'] = {'default_move_id': self.id}
        return action
    @api.depends('amount_total')
    def _compute_amount_total_text(self):
        """Compute the total amount in words for each record."""
        for record in self:
            record.amount_total_text = record._amount_to_text_custom(record.amount_total)

    def convert_amount_to_words(self, amount):
        """Convert the integer part of the amount to words in French."""
        try:
            # Convert the integer part to words using num2words
            return num2words(amount, lang='fr')
        except Exception:
            return ""

    def _amount_to_text_custom(self, amount):
        """Customized method to convert the amount to text with specific formatting."""
        # Split the amount into integer and decimal parts
        integer_part, decimal_part = divmod(round(amount * 100), 100)

        # Convert integer part to words
        integer_text = self.convert_amount_to_words(integer_part)
        integer_text = f"{integer_text} dinars"  # Append 'dinares' to the integer part

        # Convert decimal part to words
        decimal_text = self.convert_amount_to_words(decimal_part)
        decimal_text = f"{decimal_text} millimes"  # Append 'millimes' to the decimal part

        # Final formatting: Combine integer and decimal parts
        formatted_text = f"{integer_text} et {decimal_text}"
        return formatted_text.strip()

class SaleOrderAmount(models.Model):
    _inherit = 'sale.order'

    amount_total_text = fields.Char(string="Total Amount in Words", compute="_compute_amount_total_text")

    

    @api.depends('amount_total')
    def _compute_amount_total_text(self):
        """Compute the total amount in words for each record."""
        for record in self:
            record.amount_total_text = record._amount_to_text_custom(record.amount_total)

    def convert_amount_to_words(self, amount):
        """Convert the integer part of the amount to words in French."""
        try:
            # Convert the integer part to words using num2words
            return num2words(amount, lang='fr')
        except Exception:
            return ""

    def _amount_to_text_custom(self, amount):
        """Customized method to convert the amount to text with specific formatting."""
        # Split the amount into integer and decimal parts
        integer_part, decimal_part = divmod(round(amount * 100), 100)

        # Convert integer part to words
        integer_text = self.convert_amount_to_words(integer_part)
        integer_text = f"{integer_text} dinares"  # Append 'dinares' to the integer part

        # Convert decimal part to words
        decimal_text = self.convert_amount_to_words(decimal_part)
        decimal_text = f"{decimal_text} millimes"  # Append 'millimes' to the decimal part

        # Final formatting: Combine integer and decimal parts
        formatted_text = f"{integer_text} et {decimal_text}"
        return formatted_text.strip()

    def action_generate_report(self):
        """Trigger the report generation for this project."""
        report_action = self.env.ref('invoice_report.action_sale_order_report')
        return report_action.report_action(self)

class PickingCustom(models.Model):
    _inherit = 'stock.picking'

    def action_generate_report_bon_de_livraison(self):
        # Trigger the report generation for this project
        report_action = self.env.ref('invoice_report.action_delivery_note_report')
        return report_action.report_action(self)
    def action_generate_report_bon_de_return(self):
        # Trigger the report generation for this project
        report_action = self.env.ref('invoice_report.action_return_note_report')
        return report_action.report_action(self)
    
