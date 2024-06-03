# -*- coding: utf-8 -*-

import logging
import base64
import re
from lxml import etree
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORGuild(models.Model):
    _name = 'swtor.guild'
    _description = 'SWTOR Guild'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    description = fields.Html(string='Description')
    image = fields.Binary(string='Image')
    guildmaster = fields.Char(string='Guildmaster')
    character_ids = fields.One2many('swtor.character', 'guild_id', string='Characters')
    member_count = fields.Integer(string='Members', compute='_compute_member_count')

    @api.depends('character_ids')
    def _compute_member_count(self):
        for rec in self:
            rec.member_count = len(rec.character_ids)
