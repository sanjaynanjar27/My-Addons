/** @odoo-module */


/** importing all important modules while creating new template we have to set template
  importing components from correct package is most important in this file
  */

import {registry} from "@web/core/registry";
import {loadJS} from "@web/core/assets";
import {useService} from "@web/core/utils/hooks";

const {Component, onWillStart, useRef, onMounted, useEffect, onWillUnmount} = owl;

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart");
        this.actionService = useService("action");
        onWillStart(async () => {
            await loadJS(
                "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js",
            );
        });
        // Effects after changing or rendering values
        // we delete old chart and all other values then it's redirected

        useEffect(
            () => {
                this.renderChart();
                console.log("The state has been changed");
            },
            () => [this.props.config],
        );

        onMounted(() => this.renderChart());

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
    // Render Chart Function to set values to chart
    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.chartRef.el, {
            // Data is rendered to xml file
            type: this.props.type,
            data: this.props.config.data,
            options: {
                onClick: (e) => {
                    // NOTE: Check if index is activated or not
                    // on click event we can perform any action
                    const active = e.chart.getActiveElements();

                    if (active.length > 0) {
                        const label = e.chart.data.labels[active[0].index];
                        const {label_field, domain} = this.props.config;
                        let new_domain = domain ? domain : [];

                        console.log(e);
                        console.log(e.chart.getActiveElements());
                        console.log(label);
                        //NOTE: IF label includes date then we have to change
                        // domain value to start of the month to end of the month

                        if (label_field) {
                            if (label_field.includes("date")) {
                                const timeStamp = Date.parse(label);
                                const selected_month = moment(timeStamp);
                                const month_start = selected_month
                                    .startOf("month")
                                    .format("YYYY-MM-DD HH:mm:ss"); // Start of the month
                                const month_end = selected_month
                                    .endOf("month")
                                    .format("YYYY-MM-DD HH:mm:ss"); // End of the month
                                new_domain.push(
                                    ["date", ">=", month_start],
                                    ["date", "<=", month_end],
                                );
                            } else {
                                new_domain.push([label_field, "=", label]);
                            }
                        }
                        //NOTE: This will return action
                        // window including your data
                        this.actionService.doAction({
                            type: "ir.actions.act_window",
                            name: this.props.title,
                            res_model: "sale.report",
                            domain,
                            views: [
                                [false, "list"],
                                [false, "form"],
                            ],
                        });
                    } else {
                        // NOTE: If click anywhere else
                        // the index error will not be shown
                        console.log("No active elements found.");
                    }
                },
                // NOTE: Other information and
                // values to print chart
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                    title: {
                        display: true,
                        text: this.props.title,
                        position: "bottom",
                    },
                },
                scales: "scales" in this.props.config ? this.props.config.scales : {},
            },
        });
    }
}

ChartRenderer.template = "owl.ChartRenderer";
