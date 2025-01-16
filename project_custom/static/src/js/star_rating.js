/** @odoo-module */

const { Component, xml } = owl;
import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";

class StarRatingComponent extends Component {
  static template = "project_custom.StarRatingTemplate";

  constructor() {
    super(...arguments);
    this.state = useState({
      currentRating: 0,
      ratingHistory: [],
    });
  }

  setRating(rating) {
    this.state.currentRating = rating;
  }

  saveRating() {
    if (this.state.currentRating > 0) {
      this.state.ratingHistory.push(this.state.currentRating);
      this.state.currentRating = 0; // Reset current rating
    }
  }

  deleteRating(index) {
    this.state.ratingHistory.splice(index, 1); // Remove the rating at the given index
  }
}

registry
  .category("actions")
  .add("project_custom.star_rating", StarRatingComponent);
