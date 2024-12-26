odoo.define("custom_dashboard_owl.dashboard", function (require) {
  "use strict";

  const { Component, useState, useEffect } = require("owl");
  const { useService } = require("web.core");

  // The Dashboard Component
  class Dashboard extends Component {
    constructor() {
      super(...arguments);
      // State for data and loading status
      this.state = useState({
        loading: true,
        data: [],
      });
    }

    async willStart() {
      // Fetch the data to populate the dashboard (you can use Odoo models or APIs here)
      this.state.loading = true;
      const data = await this.fetchDashboardData();
      this.state.data = data;
      this.state.loading = false;
    }

    // Simulate a fetch call (replace with actual data fetch logic)
    async fetchDashboardData() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve([
            { label: "Total Sales", value: 10000 },
            { label: "Pending Orders", value: 50 },
            { label: "Completed Orders", value: 300 },
          ]);
        }, 1000);
      });
    }

    render() {
      return this.state.loading ? this.renderLoading() : this.renderDashboard();
    }

    renderLoading() {
      return `
                <div class="dashboard-loading">
                    <span>Loading...</span>
                </div>
            `;
    }

    renderDashboard() {
      return `
                <div class="dashboard-container">
                    <h1>Sales Dashboard</h1>
                    <div class="dashboard-cards">
                        ${this.state.data
                          .map(
                            (item) => `
                            <div class="dashboard-card">
                                <h3>${item.label}</h3>
                                <p>${item.value}</p>
                            </div>
                        `,
                          )
                          .join("")}
                    </div>
                </div>
            `;
    }
  }

  Dashboard.template = "custom_dashboard_owl.DashboardTemplate";

  return Dashboard;
});
