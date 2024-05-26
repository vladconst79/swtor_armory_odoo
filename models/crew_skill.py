# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORCrewSkill(models.Model):
    _name = 'swtor.crew.skill'
    _description = 'SWTOR Crew Skill'

    max_level = 700

    name = fields.Char(string='Crew Skill Name', required=True)
    # level = fields.Integer(string='Skill Level')
    skill_type = fields.Selection([
        ('crafting', 'Crafting'),
        ('gathering', 'Gathering'),
        ('mission', 'Mission')
    ], string='Skill Type', required=True)
    character_ids = fields.One2many('swtor.character.crew.skill.relation', 'crew_skill_id', string='Characters')


class CharacterCrewSkillRel(models.Model):
    _name = 'swtor.character.crew.skill.relation'
    _description = 'Character Crew Skill Relation'

    display_name = fields.Char(compute="_compute_display_name", store=True, compute_sudo=True)
    character_id = fields.Many2one('swtor.character', ondelete='cascade', required=True)
    crew_skill_id = fields.Many2one('swtor.crew.skill', ondelete='cascade', required=True)
    level = fields.Integer(string='Skill Level', default=1)
    skill_type = fields.Selection(related='crew_skill_id.skill_type')
    progress = fields.Float(string='Progress', compute='_compute_progress', store=True)

    @api.depends('level')
    def _compute_progress(self):
        for record in self:
            record.progress = record.level / self.env['swtor.crew.skill'].max_level * 100

    @api.depends('character_id.name', 'crew_skill_id.name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.character_id.name} - {record.crew_skill_id.name}"

    @api.constrains('level')
    def _check_skill_levels(self):
        for record in self:
            if not 1 <= record.level <= self.crew_skill_id.max_level:
                raise ValidationError("Profession 1 Level must be between 1 and 700.")
#