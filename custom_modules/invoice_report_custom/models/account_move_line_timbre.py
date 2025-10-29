from email.policy import default

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    apply_timbre = fields.Boolean(string='Appliquer le Timbre', default=False)
    timbre = fields.Boolean(string='Appliquer le Timbre', default=False)
    report_without_image = fields.Boolean(string='Rapport sans Image', default=False)
    reduced_amount = fields.Monetary( compute='_compute_reduced_amount', store=True)
    reduction_amount = fields.Monetary(string="Reduced Amount",  store=True)
    timbre_fiscal = fields.Monetary(
        string="Timbre fiscal",
        currency_field='currency_id',
        default=0.600,
        readonly=True
    )

    @api.depends('amount_untaxed', 'amount_tax', 'timbre_fiscal')
    def _compute_amount(self):
        """
        Override to add timbre_fiscal in total.
        """
        super(AccountMove, self)._compute_amount()
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund'):
                move.amount_total = move.amount_untaxed + move.amount_tax + move.timbre_fiscal

    @api.onchange('apply_timbre')
    def _onchange_apply_timbre(self):
        for move in self:
            if move.state != 'draft':
                continue

            # Find or create the Timbre Fiscale product
            product = self.env['product.product'].search([('name', '=', 'Timbre Fiscale')], limit=1)
            if not product:
                product = self.env['product.product'].create({
                    'name': 'Timbre Fiscale',
                    'type': 'service',
                    'sale_ok': True,
                    'purchase_ok': True,
                    'list_price': 1,
                    'standard_price': 1,
                })

            # Ensure the product has an income account
            account = product.categ_id.property_account_income_categ_id
            if not account:
                return

            if move.apply_timbre:
                # Check if the Timbre line already exists
                if not move.invoice_line_ids.filtered(lambda l: l.product_id == product):
                    move.invoice_line_ids = [(0, 0, {
                        'product_id': product.id,
                        'name': product.name,
                        'price_unit': product.list_price,
                        'quantity': 1,
                        'account_id': account.id,
                    })]
            else:
                # Remove existing Timbre lines
                move.invoice_line_ids = [(2, line.id) for line in move.invoice_line_ids.filtered(lambda l: l.product_id == product)]

    show_reduction = fields.Boolean(string="Amount total > 1000000", default=False,store=True,compute='_compute_show_reduction')

    @api.depends('amount_total')  # Depend on the amount_total field
    def _compute_reduced_amount(self):
        for record in self:
            if record.amount_total > 999999:
                # Reduce 1% of the total amount
                record.reduced_amount = record.amount_total - (record.amount_total * 0.01)
                record.show_reduction = True
            else:
                record.reduced_amount = 0  # Reset to zero when the condition is not met
                record.show_reduction = False

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        # This method is optional, it's to ensure that any manual changes are reflected
        # For example, if amount_total changes in the UI, you want the values to update accordingly
        if self.amount_total > 999999:
            self.show_reduction = True
        else:
            self.show_reduction = False

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    timbre_fiscal = fields.Boolean('Timbre fiscal', default=False)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'




