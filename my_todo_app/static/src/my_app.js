/** @odoo-module */

import TodoList  from "./js/todo_list";
import { App } from "@odoo/owl";

async function initializeTodoApp() {
    const target = document.querySelector("#todo_list_container");
    console.log("---------------target", target);
    console.log("---------------TodoList", TodoList);

    if (target) {
        const app = new App(TodoList, {
            warnIfNoStaticProps: true,
            name: TodoList.name,
        });
        const root = await app.mount(target);
        console.log("App mounted successfully:", root);
    } else {
        console.error("Target element not found in the DOM. Ensure the controller renders the template.");
    }
}
document.addEventListener("DOMContentLoaded", initializeTodoApp);
