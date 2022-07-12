from odoo import fields, models, api


class VcaCertificateType(models.Model):
    _name = 'vca.certificate_type'
    _description = 'VCA Certificate Types'

    name = fields.Char(required=True)
    certificate_ids = fields.One2many(comodel_name='vca.certificate', inverse_name='certificate_type_id')
