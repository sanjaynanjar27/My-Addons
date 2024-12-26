/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class OrderLineDeliveryNoteButton extends Component {
  static template = "point_of_sale.OrderLineDeliveryNoteButton";
  setup() {
    this.pos = usePos();
    this.popup = useService("popup");
  }
  async onClick() {
    const selectedOrderline = this.pos.get_order().get_selected_orderline();
    if (!selectedOrderline) {
      return;
    }
    const { confirmed, payload: inputNote } = await this.popup.add(
      TextAreaPopup,
      {
        startingValue: selectedOrderline.get_delivery_note(),
        title: "Add Delivery Note",
      },
    );

    if (confirmed) {
      selectedOrderline.set_delivery_note(inputNote);
    }
  }
}

ProductScreen.addControlButton({
  component: OrderLineDeliveryNoteButton,
});
