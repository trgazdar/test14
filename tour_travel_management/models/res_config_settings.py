# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_discount_id = fields.Many2one(
        'product.product',
        string='Package Discount',
        required = True
    )
    product_extra_bed_id = fields.Many2one(
        'product.product',
        string='Extra Bed',
        required = True
    )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        discount = self.env.ref('tour_travel_management.package_discount').id
        extra_bed = self.env.ref('tour_travel_management.package_extra_bed').id
        if discount:
            res.update(
                product_discount_id = discount
            )
        if extra_bed:
            res.update(
                product_extra_bed_id = extra_bed
            )
        return res
