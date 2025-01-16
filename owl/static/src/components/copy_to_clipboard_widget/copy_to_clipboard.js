/** @odoo-module **/

import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class CopyField extends Component {
    setup() {
        super.setup()
        console.log("Data is printed while Pressing Copy Button...")
        console.log(this.props.record.data.phone_number); // Check the properties passed to the widget
        console.log(this.props.record.data)
        this.actionService = useService("action");  // Initialize the action service
    }

    onCopy() {
        const value = this.props.record.data.phone_number;
        console.log(value)
        if (value) {
            console.log(value);
            navigator.clipboard.writeText(value)
                .then(() => {
                        this.actionService.doAction({
                                type: 'ir.actions.client',
                                tag: 'display_notification',
                                params: {
                                    title: 'Text Copied to Clipboard',
                                    message: 'The phone '+ value  +' number has been copied successfully!',
                                    sticky: false,
                                    type: 'info',
                                }
                            }
                        );
                    }
                )
                .catch(err => {
                    console.error('Failed to copy: ', err);
                    this.actionService.doAction({
                            type: 'ir.actions.client',
                            tag: 'display_notification',
                            params: {
                                title: 'Not Copied to Clipboard',
                                message: err,
                                sticky: false,
                                type: 'danger',
                            }
                        }
                    );
                });
        } else {
            this.actionService.doAction({
                    type: 'ir.actions.client',
                    tag: 'display_notification',
                    params: {
                        title: 'Not Copied to Clipboard',
                        message: "No Value To Copy",
                        sticky: false,
                        type: 'warning',
                    }
                }
            );
        }
    }
}

export const copyField = {
    component: CopyField,
    displayName: 'Copy Field',
    supportedTypes: ["char"],
};


CopyField.template = "owl.CopyField"
registry.category("fields").add("copy_to_clipboard", copyField);
