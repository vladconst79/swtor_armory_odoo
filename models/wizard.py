# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Greuceanu
# This file is part of SWTOR Armory and is licensed under the
# GNU Affero General Public License v3.0 or later.

from odoo import models, fields, api

class CrewSkillWizard(models.TransientModel):
    _name = 'swtor.crew.skill.wizard'
    _description = 'Crew Skill Wizard'

    crew_skill_id = fields.Many2one('swtor.crew.skill', string='Crew Skill', required=True)
    level = fields.Integer(string='Level', required=True)

    def confirm(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        self.env['swtor.character.crew.skill.relation'].create({
            'character_id': active_id,
            'crew_skill_id': self.crew_skill_id.id,
            'level': self.level,
        })
