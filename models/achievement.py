# -*- coding: utf-8 -*-

import logging
import base64
import re
from lxml import etree
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORAchievement(models.Model):
    _name = 'swtor.achievement'
    _description = 'SWTOR Achievement'

    name = fields.Char(string='Name', store=True, compute='_compute_name', index=True)
    user_id = fields.Many2one('res.users', string='User', required=True, index=True, default=lambda self: self.env.user)
    achievement_id = fields.Many2one('swtor.achievement.template', string='Achievement', required=True, index=True)
    date = fields.Datetime(string='Date', required=True, index=True, default=fields.Datetime.now)
    description = fields.Html(string='Description')
    time = fields.Float(string='Spent Time', store=True)


class SWTORAchievementTemplate(models.Model):

    _name = 'swtor.achievement.template '
    _description = 'SWTOR Achievement Template'

    name = fields.Char(string='Name', required=True)
    description = fields.Html(string='Description')
    image = fields.Binary(string='Icon')
    points = fields.Integer(string='Points')
    category_id = fields.Many2one('swtor.achievement.category', string='Category')


class SWTORAchievementCategory(models.Model):

    _name = 'swtor.achievement.category'
    _description = 'SWTOR Achievement Category'

    name = fields.Char(string='Name', required=True)
    description = fields.Html(string='Description')
    image = fields.Binary(string='Icon')
    achievement_ids = fields.One2many('swtor.achievement.template', 'category_id', string='Achievements')
    parent_id = fields.Many2one('swtor.achievement.category', string='Parent Category')
    child_ids = fields.One2many('swtor.achievement.category', 'parent_id', string='Child Categories')
    operation_id = fields.Many2one('swtor.operation', string='Operation')
    operation_difficulty_id = fields.Many2one('swtor.operation.difficulty', string='Operation Difficulty')

