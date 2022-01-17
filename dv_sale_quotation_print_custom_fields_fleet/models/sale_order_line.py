from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # ==== Business fields ====
    l10n_pe_edi_price_base = fields.Monetary(string='Subtotal without discounts', store=True, readonly=True, currency_field='currency_id', help="Total amount without discounts and taxes")
    l10n_pe_edi_price_unit_excluded = fields.Float(string='Price unit excluded', digits='Product Price', store=True, readonly=True, currency_field='currency_id', help="Price unit without taxes")
    l10n_pe_edi_price_unit_included = fields.Float(string='Price unit IGV included', digits='Product Price', store=True, readonly=True, currency_field='currency_id', help="Price unit with IGV included")
    l10n_pe_edi_amount_discount = fields.Monetary(string='Amount discount before taxes', store=True, readonly=True, currency_field='currency_id', help='Amount discount before taxes')
    l10n_pe_edi_amount_free = fields.Monetary(string='Amount free', store=True, readonly=True, currency_field='currency_id', help='amount calculated if the line id for free product')
    l10n_pe_edi_free_product = fields.Boolean('Free', store=True, readonly=True, default=False, help='Is free product?')
    l10n_pe_edi_regularization_advance = fields.Boolean(string='Regularization Advance')
    l10n_pe_edi_advance_serie = fields.Char(string='Advance Serie')
    l10n_pe_edi_advance_number = fields.Integer(string='Advance Number')
    
    # ==== Tax fields ====    
    l10n_pe_edi_igv_type = fields.Many2one('l10n_pe_edi.catalog.07', string="Type of IGV", compute='_compute_igv_type', store=True, readonly=False)
    l10n_pe_edi_isc_type = fields.Many2one('l10n_pe_edi.catalog.08', string="Type of ISC", compute='_compute_isc_type', store=True, readonly=False)
    l10n_pe_edi_igv_amount = fields.Monetary(string='IGV amount',store=True, readonly=True, currency_field='currency_id', help="Total IGV amount")
    l10n_pe_edi_isc_amount = fields.Monetary(string='ISC amount',store=True, readonly=True, currency_field='currency_id', help="Total ISC amount")
    l10n_pe_edi_icbper_amount = fields.Monetary(string='ICBPER amount',store=True, readonly=True, currency_field='currency_id', help="Total ICBPER amount")

    @api.depends('tax_id','l10n_pe_edi_free_product')
    def _compute_igv_type(self):
        for line in self:
            if line.discount >= 100.0:  
                # Discount >= 100% means the product is free and the IGV type should be 'No onerosa' and 'taxed'
                tax_id = self.env.ref('l10n_pe.1_sale_tax_gra').id
                line.l10n_pe_edi_igv_type = self.env['l10n_pe_edi.catalog.07'].search([('code','=','15')], limit=1).id
                line.tax_id = [(6,0,[tax_id])]
            elif any(tax.l10n_pe_edi_tax_code in ['1000'] for tax in line.tax_id):
                # Tax with code '1000' is IGV
                line.l10n_pe_edi_igv_type = self.env['l10n_pe_edi.catalog.07'].search([('code','=','10')], limit=1).id
            elif all(tax.l10n_pe_edi_tax_code in ['9997'] for tax in line.tax_id):
                # Tax with code '9997' is Exonerated
                line.l10n_pe_edi_igv_type = self.env['l10n_pe_edi.catalog.07'].search([('type','=','exonerated')], limit=1).id
            elif all(tax.l10n_pe_edi_tax_code in ['9998'] for tax in line.tax_id):
                # Tax with code '9998' is Unaffected
                line.l10n_pe_edi_igv_type = self.env['l10n_pe_edi.catalog.07'].search([('type','=','unaffected')], limit=1).id
            elif all(tax.l10n_pe_edi_tax_code in ['9995'] for tax in line.tax_id):
                # Tax with code '9995' is for Exportation
                line.l10n_pe_edi_igv_type = self.env['l10n_pe_edi.catalog.07'].search([('type','=','exportation')], limit=1).id
            else:
                line.l10n_pe_edi_igv_type = self.env['l10n_pe_edi.catalog.07'].search([('code','=','10')], limit=1).id
    
    @api.depends('tax_id')
    def _compute_isc_type(self):
        for line in self:
            if any(tax.l10n_pe_edi_tax_code in ['2000'] for tax in line.tax_id):
                line.l10n_pe_edi_isc_type = line.tax_id.filtered(lambda r: r.l10n_pe_edi_tax_code == '2000')[0].l10n_pe_edi_isc_type
            else:
                line.l10n_pe_edi_isc_type = False
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

            quantity = line.product_uom_qty
            price_unit = line.price_unit
            discount = line.discount
            currency = line.currency_id
            product = line.product_id
            partner = line.order_partner_id
            l10n_pe_edi_price_base = quantity * price_unit
            l10n_pe_edi_price_unit_excluded = price_unit
            l10n_pe_edi_price_unit_included = price_unit
            l10n_pe_edi_igv_amount = 0.0
            l10n_pe_edi_isc_amount = 0.0
            l10n_pe_edi_icbper_amount = 0.0
            taxes = line.tax_id
            if taxes:
                # Compute taxes for all line
                taxes_res = taxes._origin.compute_all(price_unit , quantity=quantity, currency=currency, product=product, partner=partner, is_refund=False)
                l10n_pe_edi_price_unit_excluded = l10n_pe_edi_price_unit_excluded_signed = quantity != 0 and taxes_res['total_excluded']/quantity or 0.0
                line.l10n_pe_edi_price_unit_excluded = l10n_pe_edi_price_unit_excluded   
                # Price unit whit all taxes included
                l10n_pe_edi_price_unit_included = l10n_pe_edi_price_unit_included_signed = quantity != 0 and taxes_res['total_included']/quantity or 0.0
                line.l10n_pe_edi_price_unit_included = l10n_pe_edi_price_unit_included     

                # Amount taxes after dicounts, return a dict with all taxes applied with discount incluided
                taxes_discount = taxes.compute_all(price_unit * (1 - (discount or 0.0) / 100.0), currency, quantity, product=product, partner=partner, is_refund=False)
                
                #~ With IGV taxes
                igv_taxes_ids = taxes.filtered(lambda r: r.tax_group_id.name == 'IGV')
                if igv_taxes_ids:
                    # Compute taxes per unit
                    l10n_pe_edi_price_unit_included = l10n_pe_edi_price_unit_included_signed = quantity != 0 and taxes_res['total_included']/quantity or 0.0 if igv_taxes_ids else price_unit
                    line.l10n_pe_edi_price_unit_included = l10n_pe_edi_price_unit_included
                    #~ IGV amount after discount for all line
                    l10n_pe_edi_igv_amount = sum( r['amount'] for r in taxes_discount['taxes'] if r['id'] in igv_taxes_ids.ids)
                l10n_pe_edi_price_base = l10n_pe_edi_price_base_signed = taxes_res['total_excluded']
                line.l10n_pe_edi_price_base = l10n_pe_edi_price_base 

                #~ With ISC taxes
                isc_taxes_ids = taxes.filtered(lambda r: r.tax_group_id.name == 'ISC')
                if isc_taxes_ids:
                    #~ ISC amount after discount for all line
                    l10n_pe_edi_isc_amount = sum( r['amount'] for r in taxes_discount['taxes'] if r['id'] in isc_taxes_ids.ids) 

                #~ With ICBPER taxes
                icbper_taxes_ids = taxes.filtered(lambda r: r.tax_group_id.name == 'ICBPER')
                if icbper_taxes_ids:
                    #~ ISC amount after discount for all line
                    l10n_pe_edi_icbper_amount = sum( r['amount'] for r in taxes_discount['taxes'] if r['id'] in icbper_taxes_ids.ids) 

            #~ Free amount
            if discount >= 100.0:  
                l10n_pe_edi_igv_amount = 0.0   # When the product is free, igv = 0
                l10n_pe_edi_isc_amount = 0.0   # When the product is free, isc = 0
                l10n_pe_edi_icbper_amount = 0.0   # When the product is free, icbper = 0
                l10n_pe_edi_amount_discount = 0.0  # Although the product has 100% discount, the amount of discount in a free product is 0             
                l10n_pe_edi_free_product = True
                l10n_pe_edi_amount_free = l10n_pe_edi_price_unit_included * quantity
            else:
                l10n_pe_edi_amount_discount = (l10n_pe_edi_price_unit_excluded * discount * quantity) / 100
                l10n_pe_edi_free_product = False
                l10n_pe_edi_amount_free = 0.0
            line.l10n_pe_edi_amount_discount = l10n_pe_edi_amount_discount
            line.l10n_pe_edi_amount_free = l10n_pe_edi_amount_free
            line.l10n_pe_edi_free_product = l10n_pe_edi_free_product
            line.l10n_pe_edi_igv_amount = l10n_pe_edi_igv_amount
            line.l10n_pe_edi_isc_amount = l10n_pe_edi_isc_amount
            line.l10n_pe_edi_icbper_amount = l10n_pe_edi_icbper_amount