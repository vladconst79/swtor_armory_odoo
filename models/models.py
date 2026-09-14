# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Greuceanu
# This file is part of SWTOR Armory and is licensed under the
# GNU Affero General Public License v3.0 or later.

# from odoo import models, fields, api


# class swtor_armory(models.Model):
#     _name = 'swtor_armory.swtor_armory'
#     _description = 'swtor_armory.swtor_armory'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
