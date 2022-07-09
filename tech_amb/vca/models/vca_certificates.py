from odoo import fields, models, api


class VcaCertificates(models.Model):
    _name = 'vca.certificate'
    _description = 'VCA Certificate'
    _rec_name = 'vehicle_type'

    serial_number = fields.Char('Serial Number', default='/', readonly=True)
    vehicle_type = fields.Selection([
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('minibus', 'Minibus'),
        ('microbus', 'Microbus')
    ])
    car_model = fields.Date()
    price = fields.Integer()

    @api.model
    def create(self, vals):
        obj = super(VcaCertificates, self).create(vals)
        if obj.serial_number == '/':
            number = self.env['ir.sequence'].get('vca.sequence.code') or '/'
            obj.write({'serial_number': number})
        return obj
