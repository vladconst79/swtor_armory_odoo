# -*- coding: utf-8 -*-

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class SwtorOperation(models.Model):
    _name = 'swtor.operation'
    _description = 'SWTOR Operation'

    name = fields.Char(string='Operation Name', required=True)
    short_name = fields.Char(string='Short Name', required=True)
    difficulty_ids = fields.Many2many('swtor.operation.difficulty', 'operation_difficulty_rel', 'operation_id', 'difficulty_id', string='Difficulties')
    boss_ids = fields.One2many('swtor.operation.boss', 'operation_id', string='Bosses')

class SwtorOperationDifficulty(models.Model):
    _name = 'swtor.operation.difficulty'
    _description = 'SWTOR Operation Difficulty'

    name = fields.Char(string='Difficulty', required=True)
    full_name = fields.Char(string='Full Name', required=True)
    color = fields.Integer('Color Index', default=0)
    operation_ids = fields.Many2many('swtor.operation', 'operation_difficulty_rel', 'difficulty_id', 'operation_id', string='Operations')

class SwtorOperationBoss(models.Model):
    _name = 'swtor.operation.boss'
    _description = 'SWTOR Operation Boss'

    name = fields.Char(string='Boss Name', required=True)
    sequence = fields.Integer('Sequence', default=10, store=True)
    operation_id = fields.Many2one('swtor.operation', string='Operation')