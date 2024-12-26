/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useState } from "@odoo/owl";

/**
 * Popup for displaying product sale orders.
 * Props:
 *  {
 *      saleOrderLines: Array of sale order line objects
 *  }
 */
export class ProductSalePopup extends AbstractAwaitablePopup {
  static template = "ProductSalePopupTemplate"; // Link to the XML template
  static defaultProps = {
    saleOrderLines: [],
  };

  setup() {
    super.setup();
    // Reactive state for sale order lines
    this.state = useState({
      saleOrderLines: this.props.saleOrderLines || [],
    });
  }

  /**
   * Get the product name from the product_id field.
   * @param {Array} productId - Product ID in the format [id, name].
   * @returns {string} - The product name or a placeholder.
   */
  getProductName(productId) {
    return productId ? productId[1] : "Unknown Product";
  }

  /**
   * Get the total price for a sale order line.
   * @param {number} priceUnit - Price per unit.
   * @param {number} quantity - Quantity of the product.
   * @returns {string} - Formatted total price.
   */
  getTotalPrice(priceUnit, quantity) {
    return (priceUnit * quantity).toFixed(2);
  }

  /**
   * Close the popup.
   */
  closePopup() {
    this.cancel(); // Closes the popup
  }
}
