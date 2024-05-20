# -*- coding: utf-8 -*-

from . import controllers
from . import models
import base64
from odoo import api, SUPERUSER_ID
from odoo.modules.module import get_module_resource

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
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
    difficulties = {
        "SM": "Story Mode",
        "VM": "Veteran Mode",
        "MM": "Master Mode",
    }
    for name, full_name in difficulties.items():
        env['swtor.operation.difficulty'].create({
            'name': name,
            'full_name': full_name,
        })
    operations = [
        ("Eternity Vault", "EV", ["SM", "VM"], [
            "Ancient Pylons",
            "Gharj",
            "Annihilation Droid XRR-3",
            "Infernal Council",
            "Soa, the Infernal One"
        ]),
        ("Karagga's Palace", "KP", ["SM", "VM"], [
            "Bonethrasher",
            "Jarg & Sorno",
            "Foreman Crusher",
            "G4-B3 Heavy Fabricator",
            "Karagga the Unyielding"
        ]),
        ("Explosive Conflict", "EC", ["SM", "VM", "MM"], [
            "Zorn & Toth",
            "Firebrand & Stormcaller",
            "Colonel Vorgath",
            "Warlord Kephess"
        ]),
        ("Terror From Beyond", "TFB", ["SM", "VM", "MM"], [
            "Writhing Horror",
            "Dread Guards",
            "Operator IX",
            "Kephess the Undying",
            "Terror From Beyond"
        ]),
        ("Scum and Villainy", "SV", ["SM", "VM", "MM"], [
            "Dash'roode",
            "Titan 6",
            "Thrasher",
            "Operations Chief",
            "Olok the Shadow",
            "Cartel Warlords",
            "Dread Master Styrak"
        ]),
        ("Dread Fortress", "DF", ["SM", "VM", "MM"], [
            "Nefra, Who Bars the Way",
            "Gate Commander Draxus",
            "Grob'Thok, Who Feeds the Forge",
            "Corruptor Zero",
            "Dread Master Brontes"
        ]),
        ("Dread Palace", "DP", ["SM", "VM", "MM"], [
            "Dread Master Bestia",
            "Dread Master Tyrans",
            "Dread Master Calphayus",
            "Dread Master Raptus",
            "Dread Council"
        ]),
        ("The Ravagers", "Rav", ["SM", "VM"], [
            "Sparky",
            "Bulo",
            "Torque",
            "Blaster & Master",
            "Cortanni"
        ]),
        ("Temple of Sacrifice", "ToS", ["SM", "VM"], [
            "Malaphar the Savage",
            "Sword Squadron",
            "The Underlurker",
            "Revanite Commanders",
            "Revan"
        ]),
        ("Gods From the Machine", "GftM", ["SM", "VM", "MM"], [
            "Tyth, God of Rage",
            "Aivela & Esne",
            "Nahut, God of Rage",
            "Scyva, Mother of Sorrows",
            "Izax, The Ultimate Devourer"
        ]),
        ("The Nature of Progress", "Dxun", ["SM", "VM", "MM"], [
            "The Pack Leader",
            "Breach CI-004: Lights Out",
            "Breacher CI-004: Fire Support",
            "Mutant Trandoshan Squad",
            "The Huntmaster",
            "Apex Vanguard",
        ]),
        ("R-4 Anomaly", "R4", ["SM", "VM"], [
            "IP-CPT",
            "Watchdog",
            "Lady Dominique",
            "Lord Kanoth"
        ])
    ]
    for operation_name, short_name, difficulties, bosses in operations:
        operation_record = env['swtor.operation'].create({
            'name': operation_name,
            'short_name': short_name,
        })
        for difficulty in difficulties:
            difficulty_record = env['swtor.operation.difficulty'].search([('name', '=', difficulty)], limit=1)
            if difficulty_record:
                operation_record.difficulty_ids = [(4, difficulty_record.id)]
        for sequence, boss in enumerate(bosses, start=1):
            env['swtor.operation.boss'].create({
                'name': boss,
                'operation_id': operation_record.id,
                'sequence': sequence,
            })
    origin_stories = {
        'Jedi Knight': 'force',
        'Jedi Consular': 'force',
        'Smuggler': 'tech',
        'Trooper': 'tech',
        'Sith Warrior': 'force',
        'Sith Inquisitor': 'force',
        'Bounty Hunter': 'tech',
        'Imperial Agent': 'tech',
    }
    for name, power_type in origin_stories.items():
        env['swtor.origin.story'].create({
            'name': name,
            'power_type': power_type,
        })
    advanced_classes = {
        'Jedi Guardian': 'force',
        'Jedi Sentinel': 'force',
        'Jedi Sage': 'force',
        'Jedi Shadow': 'force',
        'Gunslinger': 'tech',
        'Scoundrel': 'tech',
        'Commando': 'tech',
        'Vanguard': 'tech',
        'Sith Juggernaut': 'force',
        'Sith Marauder': 'force',
        'Sith Sorcerer': 'force',
        'Sith Assassin': 'force',
        'Sniper': 'tech',
        'Operative': 'tech',
        'Mercenary': 'tech',
        'Powertech': 'tech',
    }
    for name, power_type in advanced_classes.items():
        env['swtor.class.name'].create({
            'name': name,
            'power_type': power_type,
        })
