/** @odoo-module */

const { Component, xml } = owl;
import { registry } from "@web/core/registry";
import { useState, useEffect } from "@odoo/owl";

class MyComponent extends Component {
    static template = "owl_task.MyComponentTemplate";

    constructor() {
        super(...arguments);
        this.state = useState({
            currentList: [],
            oldLists: []
        });
    }

    onEnterKeyPress(event) {
        if (event.key === "Enter" && event.target.value.trim() !== "") {
            this.state.currentList.push(event.target.value.trim());
            event.target.value = "";
        }
    }

    onCreateNewList() {
        if (this.state.currentList.length > 0) {
            this.state.oldLists.push([...this.state.currentList]);
            this.state.currentList = [];
        }
    }

    onClickItem(event) {
        const currentStyle = event.target.style.textDecoration;
        event.target.style.textDecoration = currentStyle === "line-through" ? "" : "line-through";
    }
    onClickDelete(event) {
    const itemText = event.target.dataset.item; // Get the item's text from the data attribute

    // Ensure `oldLists` is a 2D array
    if (!Array.isArray(this.state.oldLists) || !this.state.oldLists.every(Array.isArray)) {
        console.error("state.oldLists is not a 2D array:", this.state.oldLists);
        return;
    }

    console.log("2D Array (oldLists) before deletion:", this.state.oldLists);

    let found = false;

    this.state.oldLists.forEach((list, rowIndex) => {
        const colIndex = list.indexOf(itemText);
        if (colIndex > -1) {
            console.log(`Value found: "${itemText}" at Row: ${rowIndex}, Column: ${colIndex}`);
            list.splice(colIndex, 1); // Remove the item from the sub-array
            found = true;
        }
    });

    if (found) {
        console.log("2D Array (oldLists) after deletion:", this.state.oldLists);
    } else {
        console.warn(`Item "${itemText}" not found in the 2D array.`);
    }
}
deleteListIndex(){
    console.log("Delete Button Called");
}

onEditList(){
    console.log("Edit Button Called");
}


setup() {
    useEffect(() => {
        const listItems = document.querySelectorAll("ul li span");
        listItems.forEach((item, index) => {
            item.style.color = index % 2 === 0 ? "red" : "blue";
        });
    }, () => [this.state.currentList]);
}

}

// Register the component in the actions category
registry.category("actions").add("owl_task.todo_list", MyComponent);
