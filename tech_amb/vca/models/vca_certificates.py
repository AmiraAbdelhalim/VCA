from odoo import fields, models, api
from datetime import datetime


class VcaCertificates(models.Model):
    _name = 'vca.certificate'
    _description = 'VCA Certificate'
    _rec_name = 'serial_number'

    serial_number = fields.Char('Serial Number', default='', readonly=True)
    vehicle_type = fields.Selection([
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('minibus', 'Minibus'),
        ('microbus', 'Microbus')
    ])
    car_model = fields.Selection([(str(year), str(year)) for year in range(datetime.now().year,
                                                                           (datetime.now().year - 21), -1)])
    price = fields.Integer()

    @api.model
    def create(self, vals):
        new_certificate = super(VcaCertificates, self).create(vals)
        if new_certificate.serial_number == '':
            number = self.env['ir.sequence'].get('vca.sequence.code') or ''
            new_certificate.write({'serial_number': number})
        return new_certificate
