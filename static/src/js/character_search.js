/** @odoo-module **/

import { registry } from "@web/core/registry";
import { SearchView } from "@web/search/search_view";  // Correct import path
import { useService } from "@web/core/utils/hooks";

class CharacterSearchView extends SearchView {
    setup() {
        super.setup();
        this.rpc = useService('rpc');

        this.addClassFilters();
    }

    async addClassFilters() {
        const classes = await this.rpc({
            model: 'swtor.class.name',
            method: 'search_read',
            args: [[], ['name']],
        });

        for (let i = 0; i < classes.length; i++) {
            const className = classes[i].name;
            this.props.arch.children.push({
                attrs: {
                    string: className,
                    name: 'class_' + i,
                    domain: `[('class_name_ids.name', '=', '${className}')]`,
                },
                tag: 'filter',
            });
        }

        // Trigger a rerender to update the search view
        this.render(true);
    }
}

registry.category("views").add("character_search", CharacterSearchView);
