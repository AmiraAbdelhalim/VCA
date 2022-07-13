from odoo import fields, models, api
from datetime import datetime


class VcaCertificates(models.Model):
    _name = 'vca.certificate'
    _description = 'VCA Certificate'
    _rec_name = 'serial_number'

    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('minibus', 'Mini Bus'),
        ('microbus', 'Micro Bus')
    ]
    CAR_MODEL_YEARS = [(str(year), str(year)) for year in range(datetime.now().year, (datetime.now().year - 21), -1)]

    vehicle_type = fields.Selection(VEHICLE_TYPES, default=VEHICLE_TYPES[0][0], required=True)
    motor_number = fields.Char(required=True)
    certificate_type_id = fields.Many2one(comodel_name='vca.certificate_type', required=True)
    chassis_number = fields.Char(required=True)
    traffic_department_id = fields.Many2one(comodel_name='vca.traffic_department', required=True)
    car_model = fields.Selection(CAR_MODEL_YEARS, default=CAR_MODEL_YEARS[0][0], required=True)
    customer_id = fields.Many2one(comodel_name='res.partner', required=True)
    brand_id = fields.Many2one(comodel_name='vca.brand', required=True)
    price = fields.Integer(required=True)
    serial_number = fields.Char('Serial Number', default='', readonly=True)

    @api.model
    def create(self, vals):
        new_certificate = super(VcaCertificates, self).create(vals)
        if new_certificate.serial_number == '':
            number = self.env['ir.sequence'].next_by_code('vca.sequence.code') or ''
            new_certificate.write({'serial_number': number})
        return new_certificate

    def print_certificate(self):
        return self.env.ref('vca.vca_report').report_action(self)
