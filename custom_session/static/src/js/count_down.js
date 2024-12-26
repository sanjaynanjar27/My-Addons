/* @odoo-module */
import { Component, useState } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service"; // Import jsonrpc
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session"; // Import session module
import { useService } from "@web/core/utils/hooks";

class AutoLogoutTimer extends Component {
    static template = "auto_logout_idle_user_odoo.AutoLogoutSystray";
    setup() {
        this.orm = useService("orm");
        // State initialization
        this.state = useState({
            idleTimeLeft: null, // Time left before auto-logout
        });
        this.defaultMinutes = 200;
        this.updateTimestamp = null; // Holds the updated timestamp for idle time
        this.intervalId = null; // Reference to the interval function


        this.fetchIdleTime();
    }

    async fetchIdleTime() {
        try {
            const userId = session.uid;
            console.log(userId);
            const data = await this.orm.call("res.users", "read", [
                [userId],
                ["session_count"],
            ]);

            this.defaultMinutes = Math.floor(data[0].session_count / 60);
            console.log(this.defaultMinutes);
            this.startIdleTimer(this.defaultMinutes);
        } catch (error) {
            console.error("Error fetching idle time:", error);
            this.startIdleTimer(this.defaultMinutes);
        }
    }

    startIdleTimer(minutes) {
        const now = new Date().getTime();
        const expirationTime = now + minutes * 60 * 1000; // Calculate expiration timestamp
        this.updateTimestamp = expirationTime;

        this.intervalId = setInterval(() => {
            const now = new Date().getTime();
            const distance = this.updateTimestamp - now;

            if (distance <= 0) {
                this.state.idleTimeLeft = _t("EXPIRED");
                clearInterval(this.intervalId);
                this.logoutUser();
            } else {
                this.state.idleTimeLeft = this.formatTime(distance);
            }
        }, 1000);
    }

    /**
     * Format the remaining time into a human-readable string.
     * @param {number} distance - Time in milliseconds.
     * @returns {string} - Formatted time (e.g., "5m 30s").
     */
    formatTime(distance) {
        const hours = Math.floor(distance / (1000 * 60 * 60)); // Total hours
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        return `${hours}h ${minutes}m ${seconds}s`;
    }

    /**
     * Log the user out and redirect to the login page.
     */
    logoutUser() {
        location.replace("/web/session/logout");
    }

    /**
     * Reset the timer when user activity is detected.
     */
    resetTimer() {
        const now = new Date().getTime();
        this.updateTimestamp = now + this.defaultMinutes * 60 * 1000;
    }

    /**
     * Set up event listeners for user activity to reset the timer.
     */
    setupEventListeners() {
        const resetEvents = [
            "mousemove",
            "keypress",
            "click",
            "touchstart",
            "mousedown",
        ];
        resetEvents.forEach((event) => {
            document.addEventListener(event, () => this.resetTimer());
        });
    }
}

// Register the component in the systray
export const systrayItem = {
    Component: AutoLogoutTimer,
};
registry
    .category("systray")
    .add("auto_logout_idle_user_odoo.AutoLogoutSystray", systrayItem, {
    sequence: 1,
});
