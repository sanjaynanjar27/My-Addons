/** @odoo-module */

import { Component } from "@odoo/owl";
import UserListComponent from './components/user_list_component';
import { App, whenReady } from "@odoo/owl";

console.log("main.js is loaded"); 

whenReady(async() => {
    const target = document.querySelector("#user_input_app");

    const app = new App(UserListComponent, {
    warnIfNoStaticProps : true,
    name: UserListComponent.constructor.name,
    });
    if (target) {
        const root = await app.mount(target);
        console.log("App mounted successfully:", root);
    } else {
        console.error("Target element #user_input_app not found in the DOM.");
    }
});