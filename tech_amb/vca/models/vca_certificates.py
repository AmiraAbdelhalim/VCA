from odoo import fields, models, api
from datetime import datetime


class VcaCertificates(models.Model):
    _name = 'vca.certificate'
    _description = 'VCA Certificate'
    _rec_name = 'serial_number'

    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('minibus', 'Minibus'),
        ('microbus', 'Microbus')
    ]

    CAR_MODEL_YEARS = [(str(year), str(year)) for year in range(datetime.now().year,(datetime.now().year - 21), -1)]

    serial_number = fields.Char('Serial Number', default='', readonly=True)
    vehicle_type = fields.Selection(VEHICLE_TYPES, default=VEHICLE_TYPES[0][0])
    car_model = fields.Selection(CAR_MODEL_YEARS, default=CAR_MODEL_YEARS[0][0])
    price = fields.Integer()
    certificate_type_id = fields.Many2one(comodel_name='vca.certificate_type')
    traffic_department_id = fields.Many2one(comodel_name='vca.traffic_department')
    motor_number = fields.Char()
    chassis_number = fields.Char()

    @api.model
    def create(self, vals):
        new_certificate = super(VcaCertificates, self).create(vals)
        if new_certificate.serial_number == '':
            number = self.env['ir.sequence'].get('vca.sequence.code') or ''
            new_certificate.write({'serial_number': number})
        return new_certificate
