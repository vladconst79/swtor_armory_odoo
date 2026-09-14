# SWTOR Armory

SWTOR Armory is an Odoo 16 community addon for self-hosted management of Star Wars: The Old Republic characters, guilds, inventories, crew skills, operations, lockouts, and related reference data.

It is provided free for the SWTOR community and is intended for players who want a structured, multi-user way to manage legacy and gameplay information outside the game client.

## Project Status

This repository currently contains the Odoo 16 addon implementation. A standalone FastAPI, PostgreSQL, and React Admin rebuild is currently planned.

## Features

- Manage SWTOR characters with faction, origin story, combat styles, roles, guild, server, race, alignment, level, valor rank, titles, mounts, and notes.
- Track loadouts, character items, cargo location, rarity, binding, and ownership.
- Manage crew skills with character-specific constraints.
- Track operations, difficulties, bosses, and character lockouts.
- Maintain reference data for origin stories, classes, specs, roles, crew skills, titles, mounts, and operations.
- Use SWTOR-themed icons and Odoo backend views for list, form, kanban, menu, and search workflows.
- Apply owner-based security rules for user-owned records, with a dedicated SWTOR Admin group for broader management.
- Seed reference data during installation through the module post-init hook.

## Requirements

- Odoo 16
- Python dependencies required by Odoo
- The Odoo addon dependency `web_domain_field`

## Installation

1. Place this repository in your Odoo custom addons path, for example:

   ```bash
   /opt/odoo16c/custom/addons/swtor_armory
   ```

2. Make sure Odoo is configured to load that addons path.

3. Install the required addon dependency:

   ```text
   web_domain_field
   ```

4. Restart Odoo.

5. Update the app list from Odoo.

6. Install `SWTOR Armory`.

## Updating

After pulling changes, restart Odoo and upgrade the module:

```bash
odoo-bin -d <database_name> -u swtor_armory
```

Use the correct Odoo command for your local deployment if your service wrapper or configuration file differs.

## Security Model

The module defines a `SWTOR Admin` group and owner-based rules for personal records. Normal users are intended to work with their own records, while SWTOR Admin users can manage shared reference data and broader module records.

Important owner checks are currently based on Odoo's `create_uid`, so imported or manually reassigned records should be reviewed carefully.

## Development Notes

Useful files and folders:

- `__manifest__.py` - module metadata, dependencies, loaded views, assets, and install hooks.
- `models/` - Odoo model definitions and business constraints.
- `views/` - Odoo form, list, kanban, menu, wizard, and template XML.
- `security/` - access rights and record rules.
- `static/` - CSS, JavaScript widgets, and SWTOR-themed icons.
- `migrations/` - versioned migration scripts.

## Community Intent

SWTOR Armory is a fan-made utility project. It is not affiliated with, endorsed by, sponsored by, or approved by Electronic Arts, BioWare, Lucasfilm, or Disney. Star Wars, Star Wars: The Old Republic, SWTOR, and related names and assets belong to their respective owners.

The project exists to help players organize their gameplay information and to give the community a practical base to improve together.

## Contributing

Community contributions are welcome. Good contribution areas include:

- Bug fixes
- Odoo view improvements
- Data model cleanup
- Security and access rule reviews
- Import/export helpers
- Better reference data
- Documentation
- Future standalone rebuild work

Please keep changes focused, avoid committing secrets or local environment files, and respect the ownership of SWTOR-related names, icons, and assets.

## License

This project is licensed under the GNU Affero General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
