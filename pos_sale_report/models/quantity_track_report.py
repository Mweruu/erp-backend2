import base64
from datetime import datetime

import pytz
from odoo import models, fields, api
import logging
import csv
import io

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class QuantityTrackReport(models.Model):
    _name = "quantity.track.report"
    _report_type = 'csv'
    _description = "Quantity track report"

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    user_id = fields.Many2one('res.users', default=_default_user)
    date_from = fields.Date(default=datetime.now())
    date_to = fields.Date(default=datetime.now())

    def get_quantity_report_data(self):
        data = []
        quantities = self.env['quantity.track'].search([('create_date', '>=', self.date_from),
                                                        ('create_date', '<=', self.date_to),
                                                        ])

        for quantity in quantities:
            product_id = quantity['product_id']
            q1 = quantity['new_quantity']
            q2 = quantity['initial_quantity']
            diff = int(float(q1)) - int(float(q2))
            local_tz = pytz.timezone('Etc/GMT-3')
            local_create_date = quantity['create_date'].astimezone(local_tz)
            if product_id:
                data.append({
                    'Datetime': local_create_date.strftime('%d-%m-%Y, %H:%M:%S'),
                    'Product_id': quantity['product_id'].name,
                    'User_id': quantity['create_uid'].name,
                    'Location': quantity['location'],
                    'Warehouse': quantity['warehouse_name'],
                    'Company name': quantity['company_name'],
                    'New Quantity': quantity['new_quantity'],
                    'Initial quantity': quantity['initial_quantity'],
                    'Total difference': diff,
                })

        data = {
            'records': data,
            'self': self.read()[0],
        }
        return data

    def action_print_quantity_report(self):
        report_data = self.get_quantity_report_data()
        return self.env.ref('pos_sale_report.quantity_track_report').with_context(landscape=True).report_action(None,
                                                                                                                data=report_data)

    def action_print_quantity_report_csv(self):
        report_data = self.get_quantity_report_data()
        if not report_data['records']:
            logger.info(f"No data")
            return {
                'warning': {
                    'title': 'No Data',
                    'message': 'There is no data to export.',
                },
            }
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(report_data['records'][0].keys())
        for record in report_data['records']:
            writer.writerow(record.values())
        content = output.getvalue().encode('utf-8')
        filename = 'QuantityTrack.csv'
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=ir.attachment&id={}&filename={}&field=datas&download=true&filename={}'.format(
                self.env['ir.attachment'].create({
                    'name': filename,
                    'datas': base64.b64encode(content),
                    'mimetype': 'text/csv'
                }).id,
                filename,
                filename
            ),
            'target': 'new'
        }


