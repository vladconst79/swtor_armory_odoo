# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORItem(models.Model):
    _name = "swtor.item"
    _description = "SWTOR Item"
    _order = "name asc"

    _max_cargo_bay = 8

    name = fields.Char(string="Name", required=True, index=True)
    active = fields.Boolean(string='Active', default=True)
    character_ids = fields.Many2many("swtor.character", string="Characters", copy=False)
    rarity = fields.Selection(string="Rarity", selection=[
        ("common", "Common"),
        ("uncommon", "Uncommon"),
        ("rare", "Rare"),
        ("epic", "Epic"),
        ("legendary", "Legendary"),
    ], default="common", copy=False, index=True)
    binding = fields.Selection(string="Bound", selection=[
        ("none", "None"),
        ("bind_on_pickup", "Bind on Pickup"),
        ("bind_on_equip", "Bind on Equip"),
        ("bind_on_legacy", "Bind on Legacy"),
    ], default="none", copy=False, index=True)
    bound = fields.Boolean(string="Bound", store=True, index=True, copy=False)
    cargo_hold = fields.Selection(string="Cargo Hold", selection=[
        ("cargo_hold", "Personal Cargo Hold"),
        ("cargo_hold_shared", "Legacy Cargo Hold"),
        ("cargo_hold_guild", "Guild Cargo Hold"),
    ], default="cargo_hold", copy=False, index=True)
    cargo_bay = fields.Integer(string="Cargo Bay", default=1, copy=False, index=True)

    @api.constrains('cargo_bay')
    def _check_cargo_bay(self):
        for rec in self:
            if 1 < rec.cargo_bay < self._max_cargo_bay:
                raise ValidationError(_("Cargo Bay must be in between 1 and %s" % self._max_cargo_bay))

    @api.constrains('cargo_hold', 'binding', 'bound')
    def _check_cargo_hold_binding(self):
        for rec in self:
            if rec.bound:
                if rec.cargo_hold != "cargo_hold":
                    raise ValidationError(_("Bound items must be stored in Personal Cargo Hold"))
                if rec.binding == "bind_on_legacy" and rec.cargo_hold == "cargo_hold_guild":
                    raise ValidationError(_("Bound items cannot stored in Guild Cargo Hold"))
