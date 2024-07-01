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
        'Slicing': 'gathering',
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

    env['swtor.role'].create({
        'name': 'Tank',
        'class_name_ids': [(6, 0, env['swtor.class.name'].search([('name', 'in', [
            'Jedi Guardian',
            'Jedi Shadow',
            'Vanguard',
            'Sith Juggernaut',
            'Sith Assassin',
            'Powertech',
        ])]).ids)]
    })

    env['swtor.role'].create({
        'name': 'Healer',
        'class_name_ids': [(6, 0, env['swtor.class.name'].search([('name', 'in', [
            'Jedi Sage',
            'Scoundrel',
            'Commando',
            'Sith Sorcerer',
            'Operative',
            'Mercenary',
        ])]).ids)]
    })
    env['swtor.role'].create({
        'name': 'DPS',
        'class_name_ids': [(6, 0, env['swtor.class.name'].search([]).ids)]
    })

    # Create specs
    ap = env['swtor.spec'].create({
        'name': 'Advanced Prototype',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Powertech')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    tactics = env['swtor.spec'].create({
        'name': 'Tactics',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Vanguard')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': ap.id,
    })
    ap.write({'mirror_class_id': tactics.id})
    anni = env['swtor.spec'].create({
        'name': 'Annihilation',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Marauder')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    watchman = env['swtor.spec'].create({
        'name': 'Watchman',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Sentinel')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': anni.id,
    })
    anni.write({'mirror_class_id': watchman.id})
    arsenal = env['swtor.spec'].create({
        'name': 'Arsenal',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Mercenary')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    gunnery = env['swtor.spec'].create({
        'name': 'Gunnery',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Commando')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': arsenal.id,
    })
    arsenal.write({'mirror_class_id': gunnery.id})
    bodyguard = env['swtor.spec'].create({
        'name': 'Bodyguard',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Mercenary')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Healer')]).id,
    })
    combat_medic = env['swtor.spec'].create({
        'name': 'Combat Medic',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Commando')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Healer')]).id,
        'mirror_class_id': bodyguard.id,
    })
    bodyguard.write({'mirror_class_id': combat_medic.id})
    carnage = env['swtor.spec'].create({
        'name': 'Carnage',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Marauder')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    combat = env['swtor.spec'].create({
        'name': 'Combat',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Sentinel')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': carnage.id,
    })
    carnage.write({'mirror_class_id': combat.id})
    concealment = env['swtor.spec'].create({
        'name': 'Concealment',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Operative')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    scrapper = env['swtor.spec'].create({
        'name': 'Scrapper',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Scoundrel')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': concealment.id,
    })
    concealment.write({'mirror_class_id': scrapper.id})
    corruption = env['swtor.spec'].create({
        'name': 'Corruption',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Sorcerer')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Healer')]).id,
    })
    seer = env['swtor.spec'].create({
        'name': 'Seer',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Sage')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Healer')]).id,
        'mirror_class_id': corruption.id,
    })
    corruption.write({'mirror_class_id': seer.id})
    darkness = env['swtor.spec'].create({
        'name': 'Darkness',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Assassin')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Tank')]).id,
    })
    kinetic = env['swtor.spec'].create({
        'name': 'Kinetic Combat',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Shadow')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Tank')]).id,
        'mirror_class_id': darkness.id,
    })
    darkness.write({'mirror_class_id': kinetic.id})
    deception = env['swtor.spec'].create({
        'name': 'Deception',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Assassin')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    infiltration = env['swtor.spec'].create({
        'name': 'Infiltration',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Shadow')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': deception.id,
    })
    deception.write({'mirror_class_id': infiltration.id})
    engi = env['swtor.spec'].create({
        'name': 'Engineering',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sniper')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    sabo = env['swtor.spec'].create({
        'name': 'Saboteur',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Gunslinger')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': engi.id,
    })
    engi.write({'mirror_class_id': sabo.id})
    fury = env['swtor.spec'].create({
        'name': 'Fury',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Marauder')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    conc = env['swtor.spec'].create({
        'name': 'Concentration',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Sentinel')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': fury.id,
    })
    fury.write({'mirror_class_id': conc.id})
    hatred = env['swtor.spec'].create({
        'name': 'Hatred',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Assassin')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    serenity = env['swtor.spec'].create({
        'name': 'Serenity',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Shadow')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': hatred.id,
    })
    hatred.write({'mirror_class_id': serenity.id})
    immortal = env['swtor.spec'].create({
        'name': 'Immortal',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Juggernaut')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Tank')]).id,
    })
    defense = env['swtor.spec'].create({
        'name': 'Defense',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Guardian')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Tank')]).id,
        'mirror_class_id': immortal.id,
    })
    immortal.write({'mirror_class_id': defense.id})
    io = env['swtor.spec'].create({
        'name': 'Innovative Ordnance',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Mercenary')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    ass = env['swtor.spec'].create({
        'name': 'Assault Specialist',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Commando')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': io.id,
    })
    io.write({'mirror_class_id': ass.id})
    leth = env['swtor.spec'].create({
        'name': 'Letality',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Operative')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    ruffian = env['swtor.spec'].create({
        'name': 'Ruffian',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Scoundrel')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': leth.id,
    })
    leth.write({'mirror_class_id': ruffian.id})
    lightning = env['swtor.spec'].create({
        'name': 'Lightning',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Sorcerer')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    tk = env['swtor.spec'].create({
        'name': 'Telekinetics',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Sage')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': lightning.id,
    })
    lightning.write({'mirror_class_id': tk.id})
    mad = env['swtor.spec'].create({
        'name': 'Madness',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Sorcerer')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    balance = env['swtor.spec'].create({
        'name': 'Balance',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Sage')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': mad.id,
    })
    mad.write({'mirror_class_id': balance.id})
    mm = env['swtor.spec'].create({
        'name': 'Marksmanship',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sniper')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    ss = env['swtor.spec'].create({
        'name': 'Sharpshooter',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Gunslinger')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': mm.id,
    })
    mm.write({'mirror_class_id': ss.id})
    medi = env['swtor.spec'].create({
        'name': 'Medicine',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Operative')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Healer')]).id,
    })
    saw = env['swtor.spec'].create({
        'name': 'Sawbones',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Scoundrel')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Healer')]).id,
        'mirror_class_id': medi.id,
    })
    medi.write({'mirror_class_id': saw.id})
    pyro = env['swtor.spec'].create({
        'name': 'Pyrotech',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Powertech')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    plasma = env['swtor.spec'].create({
        'name': 'Plasmatech',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Vanguard')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': pyro.id,
    })
    pyro.write({'mirror_class_id': plasma.id})
    rage = env['swtor.spec'].create({
        'name': 'Rage',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Juggernaut')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    focus = env['swtor.spec'].create({
        'name': 'Focus',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Guardian')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': rage.id,
    })
    rage.write({'mirror_class_id': focus.id})
    shield_tech = env['swtor.spec'].create({
        'name': 'Shield Tech',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Powertech')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Tank')]).id,
    })
    shield_spec = env['swtor.spec'].create({
        'name': 'Shield Specialist',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Vanguard')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'Tank')]).id,
        'mirror_class_id': shield_tech.id,
    })
    shield_tech.write({'mirror_class_id': shield_spec.id})
    veng = env['swtor.spec'].create({
        'name': 'Vengeance',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sith Juggernaut')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    vigi = env['swtor.spec'].create({
        'name': 'Vigilance',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Jedi Guardian')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': veng.id,
    })
    veng.write({'mirror_class_id': vigi.id})
    viru = env['swtor.spec'].create({
        'name': 'Virulence',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Sniper')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
    })
    df = env['swtor.spec'].create({
        'name': 'Dirty Fighting',
        'class_name_id': env['swtor.class.name'].search([('name', '=', 'Gunslinger')]).id,
        'role_id': env['swtor.role'].search([('name', '=', 'DPS')]).id,
        'mirror_class_id': viru.id,
    })
    viru.write({'mirror_class_id': df.id})
