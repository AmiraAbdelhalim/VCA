from odoo import fields, models, api


class VcaTrafficDepartment(models.Model):
    _name = 'vca.traffic_department'
    _description = 'VCA Traffic Department'

    name = fields.Char(required=True)
    certificate_ids = fields.One2many(comodel_name='vca.certificate', inverse_name='traffic_department_id')

