# -*- coding: utf-8 -*-

import logging
import base64
import mimetypes
from urllib.request import urlopen
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORVehicle(models.Model):
    _name = 'swtor.vehicle'
    _description = 'SWTOR Vehicle'

    name = fields.Char(string='Vehicle', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    source = fields.Selection([
        ('operation', 'Operation'),
        ('flashpoint', 'Flashpoint'),
        ('pvp', 'PvP'),
        ('pve', 'PvE'),
        ('space', 'Space'),
        ('cartel', 'Cartel Market'),
        ('reputation', 'Reputation'),
        ('crafting', 'Crafting'),
        ('event', 'Event'),
        ('promotion', 'Promotion'),
        ('subscription', 'Subscription'),
    ])
    bind = fields.Selection([
        ('bind_on_pickup', 'Bind on Pickup'),
        ('bind_on_equip', 'Bind on Equip'),
        ('bind_on_legacy', 'Bind on Legacy'),
        ], string='Bind Type')
    operation_id = fields.Many2one('swtor.operation', string='Operation')
    operation_difficulty_id = fields.Many2one('swtor.operation.difficulty', string='Operation Difficulty')
    character_ids = fields.Many2many('swtor.character', string='Characters', copy=False)
    # description = fields.Text(string='Description', translate=True)
    icon = fields.Binary(string='Icon')
    icon_filename = fields.Char(string='Icon Filename')
    icon_url = fields.Char(string='Icon URL')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if 'icon_url' in vals and vals['icon_url']:
            record._set_icon_from_url(vals['icon_url'])
        return record

    def write(self, vals):
        result = super().write(vals)
        if 'icon_url' in vals and vals['icon_url']:
            for record in self:
                record._set_icon_from_url(vals['icon_url'])
        return result

    def _set_icon_from_url(self, url):
        mimetype, encoding = mimetypes.guess_type(url)
        if not mimetype or not mimetype.startswith('image/'):
            _logger.error('URL does not point to an image: %s', url)
            return

        try:
            response = urlopen(url)
            data = base64.b64encode(response.read())
            filename = url.split('/')[-1]
            self.write({
                'icon': data,
                'icon_filename': filename,
            })
        except Exception as e:
            _logger.error('Error while fetching image from URL: %s', e)

