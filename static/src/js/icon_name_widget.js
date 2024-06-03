/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class IconNameWidget extends Component {
    setup() {
        this.orm = useService("orm");
        this.field = useState({
            icon: this.props.record.data[this.props.field.icon],
            name: this.props.record.data[this.props.field.name],
        });
    }

    get iconUrl() {
        return `/web/image/${this.props.model}/${this.props.record.id}/${this.props.field.icon}`;
    }
}

IconNameWidget.template = "swtor_armory.IconNameWidget";

registry.category("fields").add("icon_name_widget", IconNameWidget);

export default IconNameWidget;
