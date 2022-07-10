from odoo import fields, models, api


class VcaBrand(models.Model):
    _name = 'vca.brand'
    _description = 'VCA brands'

    name = fields.Char()
    certificate_ids = fields.One2many(comodel_name='vca.certificate', inverse_name='brand_id')

