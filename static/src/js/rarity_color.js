/** @odoo-module **/

import { registry } from "@web/core/registry";
// import { FieldSelection } from "@web/fields/selection_field";
import { SelectionField } from "@web/views/fields/selection/selection_field";

export class RarityColor extends SelectionField {
    _renderReadonly() {
        super._renderReadonly();
        const value = this.value;
        if (value) {
            this.el.classList.add('rarity-' + value[0].toLowerCase());
        }
    }
}

// Register the widget
registry.category("fields").add("rarity_color", RarityColor);

// export default RarityColor;


/*
odoo.define('swtor_armory.RarityColor', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    // var FieldSelection = fieldRegistry.get('selection');
    var FieldSelection = require('web.relational_fields').FieldSelection;

    var RarityColor = FieldSelection.extend({
        _renderReadonly: function () {
            this._super();
            var value = this.value;
            if (value) {
                this.$el.addClass('rarity-' + value[0].toLowerCase());
            }
        },
    });

    fieldRegistry.add('rarity_color', RarityColor);

    return RarityColor;
});*/
