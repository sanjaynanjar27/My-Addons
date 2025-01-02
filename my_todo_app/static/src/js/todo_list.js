/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class TodoList extends Component {
    static template = "my_todo_app.TodoListView";
    setup() {
        super.setup(...arguments);
        this.state = useState({ tasks: [], newTaskName: "" });
        const rpc = useService("rpc");
    }

    async addTask() {
        if (this.state.newTaskName.trim()) {
            const task = await rpc("/todo/tasks/add", { name: this.state.newTaskName });
            this.state.tasks.push(task);
            this.state.newTaskName = "";
        }
    }

    async toggleTask(id, completed) {
        const updatedTask = await rpc("/todo/tasks/update", { task_id: id, completed });
        const taskIndex = this.state.tasks.findIndex((t) => t.id === id);
        if (taskIndex !== -1) {
            this.state.tasks[taskIndex] = updatedTask;
        }
    }

    async removeTask(id) {
        await rpc("/todo/tasks/delete", { task_id: id });
        this.state.tasks = this.state.tasks.filter((t) => t.id !== id);
    }

    async onWillStart() {
        const tasks = await rpc("/todo/tasks");
        this.state.tasks = tasks;
    }
}
