# -*- coding: utf-8 -*-

import logging
import base64
import re
from lxml import etree
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class SWTORTitle(models.Model):
    _name = 'swtor.title'
    _description = 'SWTOR Title'

    name = fields.Char(string='Title', required=True, translate=True)
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
    type = fields.Selection([
        ('legacy', 'Legacy'),
        ('character', 'Character'),
    ])
    operation_id = fields.Many2one('swtor.operation', string='Operation')
    operation_difficulty_id = fields.Many2one('swtor.operation.difficulty', string='Operation Difficulty')

    # description = fields.Text(string='Description', translate=True)
    # icon = fields.Binary(string='Icon')
    # icon_filename = fields.Char(string='Icon Filename')
    # icon_url = fields.Char(string='Icon URL')
    # is_hidden = fields.Boolean(string='Hidden')
    # is_legacy = fields.Boolean(string='Legacy')
    # is_pvp = fields.Boolean(string='PvP')
    # is_pve = fields.Boolean(string='PvE')
    # is_space = fields.Boolean(string='Space')
    # is_cartel = fields.Boolean(string='Cartel Market')
    # is_reputation = fields.Boolean(string='Reputation')
    # is_crafting = fields.Boolean(string='Crafting')
    # is_event = fields.Boolean(string='Event')
    # is_promotion = fields.Boolean(string='Promotion')
    # is_subscription = fields.Boolean(string='Subscription

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.type == 'character':
            characters = self.env['swtor.character'].search([('create_uid', '=', self.env.user.id)])
            for character in characters:
                character.title_ids = [(4, record.id)]
        return record
