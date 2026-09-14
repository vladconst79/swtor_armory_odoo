# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Greuceanu
# This file is part of SWTOR Armory and is licensed under the
# GNU Affero General Public License v3.0 or later.

import logging
from dateutil.relativedelta import relativedelta, TU, MO
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SwtorOperation(models.Model):
    _name = 'swtor.operation'
    _description = 'SWTOR Operation'

    name = fields.Char(string='Operation Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    short_name = fields.Char(string='Short Name', required=False)
    difficulty_ids = fields.Many2many('swtor.operation.difficulty', 'operation_difficulty_rel', 'operation_id', 'difficulty_id', string='Difficulties')
    boss_ids = fields.One2many('swtor.operation.boss', 'operation_id', string='Bosses')
    title_ids = fields.One2many('swtor.title', 'operation_id', string='Titles')
    vehicle_ids = fields.One2many('swtor.vehicle', 'operation_id', string='Mounts')


class SwtorOperationDifficulty(models.Model):
    _name = 'swtor.operation.difficulty'
    _description = 'SWTOR Operation Difficulty'

    name = fields.Char(string='Difficulty', required=True)
    active = fields.Boolean(string='Active', default=True)
    full_name = fields.Char(string='Full Name', required=True)
    color = fields.Integer('Color Index', default=0)
    operation_ids = fields.Many2many('swtor.operation', 'operation_difficulty_rel', 'difficulty_id', 'operation_id', string='Operations')


class SwtorOperationBoss(models.Model):
    _name = 'swtor.operation.boss'
    _description = 'SWTOR Operation Boss'

    name = fields.Char(string='Boss Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer('Sequence', default=10, store=True)
    operation_id = fields.Many2one('swtor.operation', string='Operation')


class SWTOROperationLockout(models.Model):
    _name = 'swtor.operation.lockout'
    _description = 'SWTOR Operation Lockout'
    _order = 'week desc'

    name = fields.Char(string='Lockout', store=True, compute='_compute_name')
    active = fields.Boolean(string='Active', default=True)
    week = fields.Date(string='Week Of', default=fields.Date.today)
    character_id = fields.Many2one('swtor.character', string='Character', required=True)
    boss_id = fields.Many2one('swtor.operation.boss', string='Boss', required=True, order="sequence")
    operation_id = fields.Many2one('swtor.operation', string='Operation', required=True)
    difficulty_id = fields.Many2one('swtor.operation.difficulty', string='Difficulty', required=True)
    completion_rate = fields.Float(string='Completion Rate', compute='_compute_completion_rate', store=True, group_operator='avg')
    faction = fields.Selection(related='character_id.faction', store=True, depends=[('character_id.faction')])

    @api.depends('week')
    def _compute_after_last_tuesday(self):
        for record in self:
            last_tuesday = datetime.now() + relativedelta(weekday=TU(-1))
            record.after_last_tuesday = record.week and record.week >= last_tuesday.date()

    @api.depends('operation_id', 'week', 'difficulty_id')
    def _compute_name(self):
        for record in self:
            if record.operation_id and record.difficulty_id and record.week:
                last_tuesday = record.week + relativedelta(weekday=TU(-1))
                next_monday = record.week + relativedelta(weekday=MO(1))
                record.name = f"{record.operation_id.name} - {record.difficulty_id.name} - {last_tuesday} - {next_monday}"
            else:
                record.name = False

    @api.depends('boss_id', 'difficulty_id')
    def _compute_completion_rate(self):
        for record in self:
            record.completion_rate = 0.0
            if record.boss_id and record.difficulty_id:
                previous_bosses = self.env["swtor.operation.boss"].search([
                    ('sequence', '<', record.boss_id.sequence),
                    ('operation_id', '=', record.boss_id.operation_id.id)
                ])
                record.completion_rate = (len(previous_bosses) + 1) / len(record.boss_id.operation_id.boss_ids) * 100
            else:
                record.completion_rate = 0.0

    @api.constrains('boss_id', 'difficulty_id')
    def _check_boss_difficulty(self):
        for record in self:
            if self.search_count([
                ('character_id', '=', record.character_id.id),
                ('boss_id', '=', record.boss_id.id),
                ('difficulty_id', '=', record.difficulty_id.id),
                ('week', '=', record.week),
                ('id', '!=', record.id)
            ]):
                raise ValidationError("Character already has a lockout for this boss and difficulty this week.")
