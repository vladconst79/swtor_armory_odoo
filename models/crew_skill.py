# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORCrewSkill(models.Model):
    _name = 'swtor.crew.skill'
    _description = 'SWTOR Crew Skill'

    name = fields.Char(string='Crew Skill Name', required=True)
    level = fields.Integer(string='Skill Level')
    skill_type = fields.Selection([
        ('crafting', 'Crafting'),
        ('gathering', 'Gathering'),
        ('mission', 'Mission')
    ], string='Skill Type', required=True)
    character_ids = fields.One2many('swtor.character.crew.skill.relation', 'crew_skill_id', string='Characters')


class CharacterCrewSkillRel(models.Model):
    _name = 'swtor.character.crew.skill.relation'
    _description = 'Character Crew Skill Relation'

    character_id = fields.Many2one('swtor.character', ondelete='cascade')
    crew_skill_id = fields.Many2one('swtor.crew.skill', ondelete='cascade')
    level = fields.Integer(string='Skill Level')

    @api.constrains('level')
    def _check_skill_levels(self):
        for record in self:
            if not 1 <= record.level <= 700:
                raise ValidationError("Profession 1 Level must be between 1 and 700.")
#