odoo.define('swtor_armory.ClassNameWidget', function(require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldMany2ManyTags = require('web.relational_fields').FieldMany2ManyTags;

    var ClassNameWidget = FieldMany2ManyTags.extend({
        _render: function () {
            this._super.apply(this, arguments);

            // Add SWTOR class symbol in front of the text
            this.$el.find('.badge').each(function() {
                var id = $(this).data('id');
                var record = self.value.data.find(function(record) {
                    return record.res_id === id;
                });
                if (record) {
                    var symbolImage = "data:image/png;base64," + record.data.class_icon;
                    $(this).prepend('<img src="' + symbolImage + '" class="mr-1">');
                }
            });
        },
    });

    fieldRegistry.add('class_name_widget', ClassNameWidget);

    return ClassNameWidget;
});