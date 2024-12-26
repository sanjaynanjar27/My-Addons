/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks";
import { capitalize } from "@web/core/utils/strings";

import { Component, useState, markup } from "@odoo/owl";

// This props are added by the error handler
export const standardErrorDialogProps = {
  traceback: { type: [String, { value: null }], optional: true },
  message: { type: String, optional: true },
  name: { type: String, optional: true },
  exceptionName: { type: [String, { value: null }], optional: true },
  data: { type: [Object, { value: null }], optional: true },
  subType: { type: [String, { value: null }], optional: true },
  code: { type: [Number, String, { value: null }], optional: true },
  type: { type: [String, { value: null }], optional: true },
  close: Function, // prop added by the Dialog service
};

// -----------------------------------------------------------------------------
// Expired Session Error Dialog
// -----------------------------------------------------------------------------
export class CustomSessionExpiredDialog extends Component {
  onClick() {
    browser.location.reload();
  }
}
CustomSessionExpiredDialog.template = "cit_user_login_status.CustomSessionExpiredDialog";
CustomSessionExpiredDialog.components = { Dialog };
CustomSessionExpiredDialog.title = _t("Odoo Session FROM HERE");
CustomSessionExpiredDialog.props = { ...standardErrorDialogProps };


registry.category("error_dialogs").remove("odoo.http.SessionExpiredException");
registry
  .category("error_dialogs")
  .add("odoo.http.SessionExpiredException", CustomSessionExpiredDialog)
