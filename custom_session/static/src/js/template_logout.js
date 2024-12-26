/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class CustomTemplateAction extends Component {
    static template = "custom_template"; // Matches the template ID in XML

    // Event Handlers
    closeTemplate() {
        this.env.bus.trigger("ACTION_MANAGER:DO_ACTION", {
            type: "ir.actions.act_window_close",
        });
    }
}

// Register the component in the action registry
registry
    .category("actions")
    .add("custom_template_action", CustomTemplateAction);
export default CustomTemplateAction;
