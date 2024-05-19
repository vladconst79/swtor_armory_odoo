# -*- coding: utf-8 -*-

import logging
from odoo import models, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORCharacter(models.Model):
    _name = 'swtor.character'
    _description = 'SWTOR Character'

    name = fields.Char(string='Character Name', required=True)
    faction = fields.Selection([
        ('republic', 'Republic'),
        ('empire', 'Empire')
    ], string='Faction', required=True)
    origin_story = fields.Selection([
        ('jedi_knight', 'Jedi Knight'),
        ('jedi_consular', 'Jedi Consular'),
        ('smuggler', 'Smuggler'),
        ('trooper', 'Trooper'),
        ('sith_warrior', 'Sith Warrior'),
        ('sith_inquisitor', 'Sith Inquisitor'),
        ('bounty_hunter', 'Bounty Hunter'),
        ('imperial_agent', 'Imperial Agent'),
        # Add more classes as needed
    ], string='Class', required=True)
    class_name = fields.Selection([
        ('guardian', 'Guardian'),
        ('sentinel', 'Sentinel'),
        ('sage', 'Sage'),
        ('shadow', 'Shadow'),
        ('gunslinger', 'Gunslinger'),
        ('scoundrel', 'Scoundrel'),
        ('commando', 'Commando'),
        ('vanguard', 'Vanguard'),
        ('juggernaut', 'Juggernaut'),
        ('marauder', 'Marauder'),
        ('sorcerer', 'Sorcerer'),
        ('assassin', 'Assassin'),
        ('sniper', 'Sniper'),
        ('operative', 'Operative'),
        ('mercenary', 'Mercenary'),
        ('powertech', 'Powertech'),
    ], string='Advanced Class', required=True)
    level = fields.Integer(string='Level')
    race = fields.Char(string='Race')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    server = fields.Selection([
        ('darth_malgus', 'Darth Malgus'),
        ('starforge', 'Star Forge'),
        ('satele_shan', 'Satele Shan'),
        ('the_leviathan', 'The Leviathan'),
        ('tulak_hord', 'Tulak Hord'),
        ('shae_vizla', 'Shae Vizla'),
    ], string='Server')
    guild = fields.Char(string='Guild')
    alignment = fields.Selection([
        ('light', 'Light'),
        ('neutral', 'Neutral'),
        ('dark', 'Dark')
    ], string='Alignment')
    crew_skills_ids = fields.Many2many('swtor.crew_skill', relation='character.crew_skill.rel', column1='character_id', column2='crew_skill_id', string='Crew Skills')
    notes = fields.Html(string='Notes')

    @api.constrains('crew_skills_ids')
    def _check_crew_skills(self):
        for record in self:
            if len(record.crew_skills_ids) > 3:
                raise ValidationError("A character can have no more than 3 crew skills.")
            if len([skill for skill in record.crew_skills_ids if skill.skill_type == 'crafting']) > 1:
                raise ValidationError("A character can have no more than 1 crafting skill.")

