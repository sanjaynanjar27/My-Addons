/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";

/**
 * Props:
 *  {
 *      category: {string} - The category name of the product
 *      product: {object} - The product object (optional, if you need to display product details)
 *  }
 */
export class ProductCategoryPopup extends AbstractAwaitablePopup {
  static template = "point_of_sale.ProductCategoryPopup";
  static defaultProps = { confirmKey: false };

  setup() {
    super.setup();
    this.pos = usePos(); // Access POS state via hook
    Object.assign(this, this.props); // Merge the category and product data into the class instance
  }

  // You could add additional methods here, like searching for other products within the category
  searchProductInCategory(productName) {
    this.pos.setSelectedCategoryId(0); // Reset selected category (if needed)
    this.pos.searchProductWord = productName; // Set the search query for the product name
    this.cancel(); // Close the popup after search
  }

  // Example of a method to display additional information for managers (optional)
  _hasCategoryAccessRights() {
    const isCategoryAccessibleToEveryUser =
      this.pos.config.is_category_accessible_to_every_user;
    const isCashierManager = this.pos.get_cashier().role === "manager";
    return isCategoryAccessibleToEveryUser || isCashierManager;
  }
}
