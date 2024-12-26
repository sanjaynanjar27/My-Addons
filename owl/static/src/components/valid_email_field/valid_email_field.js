/** @odoo-module */

import {registry} from "@web/core/registry"
import {EmailField} from "@web/views/fields/email/email_field";


class ValidEmailField extends EmailField {
    setup() {
        super.setup()
        console.log("Data is printed while calling widget")
        console.log(this.props.record.data.email); // Check the properties passed to the widget
    }

    // get isValidEmail(){
    //     let re = /\S+@\S+.\S+/;
    //     return re.test(this.props.record.data.email)
    // }

    get isValidEmail() {
        const email = this.props.record?.data?.email;
        if (!email) return false;
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        const isValidFormat = re.test(email);

        if (!isValidFormat) return false;

        if (email.length > 254) return false;

        const [localPart, domain] = email.split('@');

        if (localPart.length > 64) return false;

        if (/\.{2,}/.test(domain)) return false;
        if (domain.startsWith('.') || domain.endsWith('.')) return false;
        return true;
    }
}

export const emailField = {
    component: ValidEmailField,
    displayName: "Email",
    supportedTypes: ["char"],
};

class FormEmailField extends EmailField {
    static template = "owl.ValidEmailField";
}

export const formEmailField = {
    ...emailField,
    component: FormEmailField,
};

ValidEmailField.template = "owl.ValidEmailField"
registry.category("fields").add("valid_email", emailField)
// registry.category("fields").add("form.valid_email", formEmailField);
