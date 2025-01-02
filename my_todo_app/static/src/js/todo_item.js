/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "my_todo_app.TodoItemView";

    static props = {
        task: { type: Object },
        onToggle: { type: Function },
        onRemove: { type: Function },
    };

    toggleTask() {
        this.props.onToggle(this.props.task.id, !this.props.task.completed);
    }

    removeTask() {
        this.props.onRemove(this.props.task.id);
    }
}
