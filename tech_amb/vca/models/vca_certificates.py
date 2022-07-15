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
    print_history_ids = fields.One2many(comodel_name='vca.print.certificate.history', inverse_name='certificate_id')
    certificate_printed = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        new_certificate = super(VcaCertificates, self).create(vals)
        if new_certificate.serial_number == '':
            number = self.env['ir.sequence'].next_by_code('vca.sequence.code') or ''
            new_certificate.write({'serial_number': number})
        return new_certificate

    def print_certificate(self):
        self.print_history()
        return self.env.ref('vca.vca_report').report_action(self)

    def print_history(self):
        user_is_normal_user = self.env['res.users'].has_group('vca.vca_normal_user_group')
        if user_is_normal_user:
            self.certificate_printed = True
            self.env['vca.print.certificate.history'].create({
                'allow_reprint': False,
                'certificate_id': self.id
            })

    def allowed_reprint(self):
        user_is_supervisor = self.env['res.users'].has_group('vca.vca_supervisor_group')
        if user_is_supervisor:
            record_to_reprint = self.env['vca.print.certificate.history'].search([('certificate_id', '=', self.id)],
                                                                                 limit=1, order='create_date desc')
            if not record_to_reprint.allow_reprint:
                self.certificate_printed = False
                vals = {'allow_reprint': True}
                record_to_reprint.write(vals)


class VcaPrintCertificateHistory(models.Model):
    _name = 'vca.print.certificate.history'
    _description = 'Track Print certificate History'

    allow_reprint = fields.Boolean()
    certificate_id = fields.Many2one(comodel_name='vca.certificate')
