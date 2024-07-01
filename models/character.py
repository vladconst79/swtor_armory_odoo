# -*- coding: utf-8 -*-
import json
import logging
import base64
import re
from lxml import etree
from odoo import models, fields, api, _, tools
from odoo.modules.module import get_resource_path
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SWTORCharacter(models.Model):
    _name = 'swtor.character'
    _description = 'SWTOR Character'
    _order = 'level desc, id asc'

    _max_level = 80
    _max_valor_rank = 100
    _max_loadouts = 10

    name = fields.Char(string='Character Name', required=True, copy=False, index=True, default=lambda self: _('New'))
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True, compute_sudo=True)
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer('Sequence', default=10, store=True)
    faction = fields.Selection([
        ('republic', 'Republic'),
        ('empire', 'Empire')
    ], string='Faction', required=True)
    origin_story_id = fields.Many2one('swtor.origin.story', string='Origin Story')
    class_name_ids = fields.Many2many('swtor.class.name', string='Advanced Classes')
    level = fields.Integer(string='Level')
    race = fields.Selection([
        ('human', 'Human'),
        ('cyborg', 'Cyborg'),
        ('pure_blood', 'Sith Pureblood'),
        ('chiss', 'Chiss'),
        ('miraluka', 'Miraluka'),
        ('mirialan', 'Mirialan'),
        ('twilek', 'Twi\'lek'),
        ('zabrak', 'Zabrak'),
        ('rattataki', 'Rattataki'),
        ('togruta', 'Togruta'),
        ('cathar', 'Cathar'),
        ('nautolan', 'Nautolan'),
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
    ], string='Server', group_operator='count')
    guild = fields.Char(string='Guild')
    guild_id = fields.Many2one('swtor.guild', string='Guild', copy=False, index=True)
    alignment = fields.Selection([
        ('light', 'Light'),
        ('neutral', 'Neutral'),
        ('dark', 'Dark')
    ], string='Alignment')
    crew_skills_ids = fields.One2many('swtor.character.crew.skill.relation', 'character_id', string='Crew Skills')
    notes = fields.Html(string='Notes')
    faction_icon = fields.Binary(string='Faction Icon', compute='_compute_faction_icon')
    operation_lockouts_ids = fields.One2many('swtor.operation.lockout', 'character_id', string='Operation Lockouts')
    valor_rank = fields.Integer(string='Valor Rank')
    crew_skills_count = fields.Integer(string='Crew Skills Count', compute='_compute_crew_skills_count', store=True)
    loadout_ids = fields.One2many('swtor.loadout', 'character_id', string='Loadouts')
    item_ids = fields.Many2many('swtor.item', string='Items')
    vehicle_ids = fields.Many2many('swtor.vehicle', string='Mounts')
    mounts = fields.Integer(string='Mounts Count', store=True, compute='_compute_mounts')
    title_ids = fields.Many2many('swtor.title', string='Titles')
    titles = fields.Integer(string='Titles Count', compute='_compute_titles', store=True)
    guild_image = fields.Binary(related="guild_id.image")
    available_role_ids = fields.Many2many('swtor.role', string='Roles', store=True, compute='_compute_roles', relation='swtor_character_available_role_rel', readonly=True)
    role_ids = fields.Many2many('swtor.role', string='Roles', domain="[('id', 'in', available_role_ids)]", relation='swtor_character_role_rel')

    @api.depends('class_name_ids')
    def _compute_roles(self):
        for record in self:
            record.available_role_ids = record.class_name_ids.mapped('role_ids')

    @api.depends('title_ids')
    def _compute_titles(self):
        for record in self:
            record.titles = len(record.title_ids)

    @api.depends('vehicle_ids')
    def _compute_mounts(self):
        for record in self:
            record.mounts = len(record.vehicle_ids)


    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'level' in fields:
            fields.remove('level')
        return super(SWTORCharacter, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    @api.constrains('loadout_ids')
    def _check_loadouts(self):
        for record in self:
            if len(record.loadout_ids) > self._max_loadouts:
                raise ValidationError(f"A character can have no more than {self._max_loadouts} loadouts.")

    @api.depends('crew_skills_ids')
    def _compute_crew_skills_count(self):
        for record in self:
            record.crew_skills_count = len(record.crew_skills_ids)

    @api.constrains('level')
    def _check_level(self):
        for record in self:
            if record.level < 1 or record.level > self._max_level:
                raise ValidationError(f"Level must be between 1 and {self._max_level}.")

    @api.constrains('valor_rank')
    def _check_valor_rank(self):
        for record in self:
            if record.valor_rank < 1 or record.valor_rank > self._max_valor_rank:
                raise ValidationError(f"Valor Rank must be between 1 and {self._max_valor_rank}.")

    @api.depends('name', 'guild_id.name')
    def _compute_display_name(self):
        for record in self:
            if record.name:
                record.display_name = f"[{record.guild_id.name}] {record.name}" if record.guild_id.name else record.name

    @api.depends('faction')
    def _compute_faction_icon(self):
        for record in self:
            if record.faction:
                if record.faction == 'empire':
                    image_path = get_resource_path('swtor_armory', 'static/src/icon/swtor_empire_icon.png')
                    with open(image_path, "rb") as image_file:
                        record.faction_icon = tools.image_process(base64.b64encode(image_file.read()))
                elif record.faction == 'republic':
                    image_path = get_resource_path('swtor_armory', 'static/src/icon/swtor_republic_icon.png')
                    with open(image_path, "rb") as image_file:
                        record.faction_icon = tools.image_process(base64.b64encode(image_file.read()))
            else:
                record.faction_icon = False

    @api.constrains('crew_skills_ids')
    def _check_crew_skills(self):
        for record in self:
            if len(record.crew_skills_ids) > 3:
                raise ValidationError("A character can have no more than 3 crew skills.")
            if len([skill for skill in record.crew_skills_ids if skill.skill_type == 'crafting']) > 1:
                raise ValidationError("A character can have no more than 1 crafting skill.")

    @api.constrains('class_name_ids')
    def _check_class_names(self):
        for record in self:
            if len(record.class_name_ids) > 2:
                raise ValidationError("A character can have no more than 2 class names.")
            if any(class_name.power_type != record.origin_story_id.power_type for class_name in record.class_name_ids):
                raise ValidationError("Class names must have the same power type as the origin story.")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super().fields_view_get(view_id, view_id, view_type, toolbar, submenu)
        doc = etree.XML(result['arch'])
        node = doc.find(f".//field[@name='class_name_ids']")
        if node is not None:
            node.set('domain', "[('power_type', '=', origin_story_id.power_type)]")
        result['arch'] = etree.tostring(doc, encoding='unicode')
        return result

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super(SWTORCharacter, self).get_view(view_id, view_type, **options)
        if view_type == 'kanban':
            _logger.debug("Customizing kanban view for swtor.character")
        # if view_type == 'search':
        #     _logger.info("Customizing search view for tt_voice.picking")
        #     # Fetch warehouses using search_read to get id and name
        #     warehouses = self.env['tt_voice.warehouse'].search_read([], ['id', 'name'])
        #
        #     # Create separator and warehouse filters
        #     separator = '<separator string="Warehouses"/>'
        #     filters = ''.join(
        #         '<filter string="%(name)s" name="warehouse_%(id)s" domain="[(\'warehouse_id\', \'=\', %(id)d)]"/>' % {
        #             'name': warehouse['name'],
        #             'id': warehouse['id']
        #         }
        #         for warehouse in warehouses
        #     )
        #
        #     # Insert the filters at the end of the search view
        #     arch = res['arch']
        #     arch = arch.replace('</search>', separator + filters + '</search>')
        #     res['arch'] = arch
        return res

    def set_guild_id(self):
        for character in self:
            # Check if the character has the 'guild' field set
            if character.guild:
                # Search for the guild in the 'swtor.guild' model
                guild = self.env['swtor.guild'].search([('name', '=', character.guild)], limit=1)

                # If the guild is found, set the 'guild_id' field of the character to the guild's id
                if guild:
                    character.guild_id = guild.id
                else:
                    # If the guild is not found, create a new guild with the same name and set the 'guild_id' field of the character to the new guild's id
                    new_guild = self.env['swtor.guild'].create({'name': character.guild})
                    character.guild_id = new_guild.id


class SWTOROriginStory(models.Model):
    _name = 'swtor.origin.story'
    _description = 'SWTOR Origin Story'

    name = fields.Char(string='Origin Story', required=True)
    active = fields.Boolean(string='Active', default=True)
    power_type = fields.Selection([
        ('force', 'Force'),
        ('tech', 'Tech')
    ], string='Power Type', required=True)
    character_ids = fields.One2many('swtor.character', 'origin_story_id', string='Characters')


class SWTORClassName(models.Model):
    _name = 'swtor.class.name'
    _description = 'SWTOR Class Name'

    name = fields.Char(string='Class Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    power_type = fields.Selection([
        ('force', 'Force'),
        ('tech', 'Tech')
    ], string='Power Type', required=True)
    all_character_ids = fields.Many2many('swtor.character', string="Characters")
    class_icon = fields.Binary(string='Class Icon')
    role_ids = fields.Many2many('swtor.role', string='Roles')
    spec_ids = fields.One2many('swtor.spec', 'class_name_id', string='Combat Styles')

    @api.depends('character_ids', 'second_character_ids')
    def _compute_all_character_ids(self):
        for record in self:
            record.all_character_ids = record.character_ids | record.second_character_ids


class SWTORSpec(models.Model):
    _name = 'swtor.spec'
    _description = 'SWTOR Combat Style'

    name = fields.Char(string='Combat Style', required=True)
    role_id = fields.Many2one('swtor.role', string='Role', required=True)
    class_name_id = fields.Many2one('swtor.class.name', string='Class Name', required=True)
    color = fields.Integer('Color Index', related='role_id.color')
    icon = fields.Binary(string='Spec Icon', related='role_id.icon')
    mirror_spec_id = fields.Many2one('swtor.spec', string='Mirror Spec')
    loadout_ids = fields.One2many('swtor.loadout', 'spec_id', string='Loadouts')


class SWTORRole(models.Model):
    _name = 'swtor.role'
    _description = 'SWTOR Role'

    name = fields.Char(string='Role', required=True)
    active = fields.Boolean(string='Active', default=True)
    class_name_ids = fields.Many2many('swtor.class.name', string='Class Names')
    icon = fields.Binary(string='Role Icon', compute='_compute_role_icon')
    color = fields.Integer('Color Index', default=0)

    @api.depends('name')
    def _compute_role_icon(self):
        for record in self:
            if record.name:
                if record.name == 'Tank':
                    image_path = get_resource_path('swtor_armory', 'static/src/icon/role-tank.png')
                    with open(image_path, "rb") as image_file:
                        record.icon = tools.image_process(base64.b64encode(image_file.read()))
                elif record.name == 'Healer':
                    image_path = get_resource_path('swtor_armory', 'static/src/icon/role-heals.png')
                    with open(image_path, "rb") as image_file:
                        record.icon = tools.image_process(base64.b64encode(image_file.read()))
                elif record.name == 'DPS':
                    image_path = get_resource_path('swtor_armory', 'static/src/icon/role-dps.png')
                    with open(image_path, "rb") as image_file:
                        record.icon = tools.image_process(base64.b64encode(image_file.read()))
            else:
                record.icon = False


class SwtorLoadout(models.Model):
    _name = 'swtor.loadout'
    _description = 'SWTOR Loadout'
    _order = 'id asc'

    name = fields.Char(string='Loadout Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    character_id = fields.Many2one('swtor.character', string='Character', required=True)
    sequence = fields.Integer('Sequence', default=10, store=True)
    loadout_type = fields.Selection([
        ('pve', 'PvE'),
        ('pvp', 'PvP')
    ], string='Loadout Type', required=True)
    # loadout_items_ids = fields.One2many('swtor.loadout.item', 'loadout_id', string='Loadout Items')
    loadout_url = fields.Char(string='Loadout URL', store=True)
    loadout_iframe = fields.Html(string='Parsely Loadout', compute='_compute_loadout_iframe', store=True, sanitize=False)
    notes = fields.Html(string='Notes')
    character_role_ids = fields.Many2many('swtor.role', string='Character Roles', related="character_id.role_ids")
    # role_id = fields.Many2one('swtor.role', string='Role', store=True, domain="[('id', 'in', character_role_ids)]")
    role_id = fields.Many2one('swtor.role', string='Role', related="spec_id.role_id", store=True)
    role_icon = fields.Binary(string='Role Icon', related="role_id.icon")
    spec_id_domain = fields.Char(string='Available Combat Styles', compute='_compute_available_spec_ids', store=True)
    spec_id = fields.Many2one('swtor.spec', string='Combat Style')

    @api.depends('character_id', 'character_role_ids')
    def _compute_available_spec_ids(self):
        for record in self:
            record.spec_id_domain = json.dumps([
                ("id", "in", record.character_id.class_name_ids.spec_ids.ids),
                ("role_id", "in", record.character_role_ids.ids)
            ])

    @api.depends('loadout_url')
    def _compute_loadout_iframe(self):
        for record in self:
            if record.loadout_url:
                _logger.debug(f'<iframe src="{record.loadout_url}" width="100%" height="600"></iframe>')
                record.loadout_iframe = f'<iframe src="{record.loadout_url}" width="100%" height="600"></iframe>'

    def open_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'swtor.loadout',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('swtor_armory.view_loadout_form').id,
            'target': 'current',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'readonly'}}},
        }

    @api.constrains('loadout_url')
    def _check_loadout_url(self):
        pattern = r'^https://parsely\.io/parser/combat-styles/[a-z]+/[A-Za-z0-9+/=]+$'
        for record in self:
            if record.loadout_url and not re.match(pattern, record.loadout_url):
                # Check if the base64 part decodes into 8 figures between 1 and 3
                base64_part = record.loadout_url.split('/')[-1]
                try:
                    decoded = base64.b64decode(base64_part).decode()
                    if not re.match(r'^[1-3]{8}$', decoded):
                        raise ValidationError("The base64 part of the loadout_url field must decode into 8 figures between 1 and 3.")
                except Exception:
                    raise ValidationError("The loadout_url field must be a valid Parsely link.")

