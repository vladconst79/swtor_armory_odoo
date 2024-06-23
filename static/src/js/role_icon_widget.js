// static/src/js/role_icon_widget.js

/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class RoleIconWidget extends Component {
    setup() {
        this.roleIcons = this.props.record.data.role_ids.records.map(role => role.data.icon);
    }
}

RoleIconWidget.template = "swtor_armory.RoleIconWidgetTemplate";

registry.category("fields").add("role_icon_widget", RoleIconWidget);
