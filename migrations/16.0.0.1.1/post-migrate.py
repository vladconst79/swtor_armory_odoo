# migrations/16.0.0.1.1/post-migrate.py
#
# Copyright (C) 2026 Greuceanu
# This file is part of SWTOR Armory and is licensed under the
# GNU Affero General Public License v3.0 or later.
def migrate(cr, registry):
    cr.execute("""
               INSERT INTO swtor_character_loadout_rel (character_id, loadout_id)
               SELECT character_id, id
               FROM swtor_loadout
               WHERE character_id IS NOT NULL
                   ON CONFLICT DO NOTHING
               """)
