# -*- coding: utf-8 -*-
import json
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORCrewSkill(models.Model):
    _name = 'swtor.crew.skill'
    _description = 'SWTOR Crew Skill'

    max_level = 700

    name = fields.Char(string='Crew Skill Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    # level = fields.Integer(string='Skill Level')
    skill_type = fields.Selection([
        ('crafting', 'Crafting'),
        ('gathering', 'Gathering'),
        ('mission', 'Mission')
    ], string='Skill Type', required=True)
    character_ids = fields.One2many('swtor.character.crew.skill.relation', 'crew_skill_id', string='Characters')
    related_crew_skill_ids = fields.Many2many('swtor.crew.skill', 'swtor_crew_skill_rel', 'skill_id', 'related_id', string='Related Crew Skills')
    related_crew_skill_domain = fields.Char(compute='_compute_related_crew_skill_domain', readonly=True, store=False, compute_sudo=True)

    @api.depends('skill_type')
    def _compute_related_crew_skill_domain(self):
        for record in self:
            if record.skill_type == 'crafting':
                record.related_crew_skill_domain = json.dumps([('skill_type', 'in', ['gathering', 'mission'])])
            else:
                record.related_crew_skill_domain = json.dumps([('skill_type', '=', 'crafting')])

    @api.constrains('related_crew_skill_ids')
    def _check_related_crew_skills(self):
        for record in self:
            if record.skill_type == 'crafting':
                pass
                if len(record.related_crew_skill_ids) > 2:
                    _logger.warn(f"You can't have more than 2 related crew skills. Selected {len(record.related_crew_skill_ids)}.")
                    # raise ValidationError("You can't have more than 2 related crew skills.")
            else:
                if 'crafing' in record.related_crew_skill_ids.mapped('skill_type'):
                    raise ValidationError("Gathering and Mission skills must be related to a Crafting skill.")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if 'related_crew_skill_ids' in vals:
            for skill in record.related_crew_skill_ids:
                if record not in skill.related_crew_skill_ids:
                    skill.related_crew_skill_ids |= record
        return record

    def write(self, vals):
        super().write(vals)
        if 'related_crew_skill_ids' in vals:
            for record in self:
                for skill in record.related_crew_skill_ids:
                    if record not in skill.related_crew_skill_ids:
                        skill.related_crew_skill_ids |= record
        return True


class CharacterCrewSkillRel(models.Model):
    _name = 'swtor.character.crew.skill.relation'
    _description = 'Character Crew Skill Relation'

    display_name = fields.Char(compute="_compute_display_name", store=True, compute_sudo=True)
    active = fields.Boolean(string='Active', default=True)
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


# ToDO: verifica sa nu aiba mai mult de 3 crew skills

