# -*- coding: utf-8 -*-

from . import controllers
from . import models
import base64
from odoo import api, SUPERUSER_ID
from odoo.modules.module import get_module_resource

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
#     icon_paths = {
#         'swtor_empire_icon': get_module_resource('swtor_armory', 'static', 'src', 'icon', 'swtor_empire_icon.png'),
#         'swtor_republic_icon': get_module_resource('swtor_armory', 'static', 'src', 'icon', 'swtor_republic_icon.png'),
#     }
#     for icon_name, icon_path in icon_paths.items():
#         with open(icon_path, "rb") as image_file:
#             encoded_image = base64.b64encode(image_file.read())
#             env['ir.attachment'].create({
#                 'name': icon_name,
#                 'datas': encoded_image,
#                 'res_model': 'swtor.character',
#                 'mimetype': 'image/png',
#             })
    crew_skills = {
        'Armormech': 'crafting',
        'ArmsTech': 'crafting',
        'Artifice': 'crafting',
        'Biochem': 'crafting',
        'Cybertech': 'crafting',
        'Synthweaving': 'crafting',
        'Slicing': 'mission',
        'Scavenging': 'gathering',
        'Bioanalysis': 'gathering',
        'Archaeology': 'gathering',
        'Underworld Trading': 'mission',
        'Diplomacy': 'mission',
        'Investigation': 'mission',
        'Treasure Hunting': 'mission',
        # Add more crew skills if needed
    }
    for skill, skill_type in crew_skills.items():
        env['swtor.crew.skill'].create({
            'name': skill,
            'skill_type': skill_type,
        })
