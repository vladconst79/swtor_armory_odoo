# -*- coding: utf-8 -*-

import logging
import base64
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORCharacter(models.Model):
    _name = 'swtor.character'
    _description = 'SWTOR Character'

    name = fields.Char(string='Character Name', required=True)
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True, compute_sudo=True)
    active = fields.Boolean(string='Active', default=True)
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
    ], string='Origin Story', required=True)
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
    race = fields.Selection([
        ('human', 'Human'),
        ('cyborg', 'Cyborg'),
        ('chiss', 'Chiss'),
        ('mirialan', 'Mirialan'),
        ('twilek', 'Twi\'lek'),
        ('zabrak', 'Zabrak'),
        # Add more races as needed...
    ], string='Race')
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
    crew_skills_ids = fields.One2many('swtor.character.crew.skill.relation', 'character_id', string='Crew Skills')
    # crew_skills_ids = fields.Many2many('swtor.character.crew.skill.relation', column1='character_id', column2='crew_skill_id', string='Crew Skills')
    notes = fields.Html(string='Notes')
    faction_icon = fields.Binary(string='Faction Icon', compute='_compute_faction_icon')
    # faction_icon = fields.Many2one('ir.attachment', string='Faction Icon', compute='_compute_faction_icon')
    # faction_icon_html = fields.Html(string='Faction Icon HTML', compute='_compute_faction_icon_html')

    @api.depends('name', 'guild')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.guild}] {record.name}" if record.guild else record.name

    @api.depends('faction')
    def _compute_faction_icon(self):
        for record in self:
            if record.faction == 'empire':
                image_path = get_resource_path('swtor_armory', 'static/src/icon/swtor_empire_icon.png')
                with open(image_path, "rb") as image_file:
                    record.faction_icon = tools.image_process(base64.b64encode(image_file.read()))
            elif record.faction == 'republic':
                image_path = get_resource_path('swtor_armory', 'static/src/icon/swtor_republic_icon.png')
                with open(image_path, "rb") as image_file:
                    record.faction_icon = tools.image_process(base64.b64encode(image_file.read()))

    # @api.depends('faction')
    # def _compute_faction_icon(self):
    #     for record in self:
    #         if record.faction:
    #             if record.faction == 'empire':
    #                 swtor_empire_icon = self.env["ir.attachment"].sudo().search([('name', '=', 'swtor_empire_icon')])
    #                 if swtor_empire_icon:
    #                     record.faction_icon = swtor_empire_icon.id
    #             elif record.faction == 'republic':
    #                 swtor_republic_icon = self.env["ir.attachment"].sudo().search([('name', '=', 'swtor_republic_icon')])
    #                 if swtor_republic_icon:
    #                     record.faction_icon = swtor_republic_icon.id
    #
    # @api.depends('faction_icon')
    # def _compute_faction_icon_html(self):
    #     for record in self:
    #         if record.faction_icon:
    #             record.faction_icon_html = '<img src="data:image/png;base64,%s" style="max-height: 60px;"/>' % record.faction_icon.datas.decode()

    @api.constrains('crew_skills_ids')
    def _check_crew_skills(self):
        for record in self:
            if len(record.crew_skills_ids) > 3:
                raise ValidationError("A character can have no more than 3 crew skills.")
            if len([skill for skill in record.crew_skills_ids if skill.skill_type == 'crafting']) > 1:
                raise ValidationError("A character can have no more than 1 crafting skill.")

