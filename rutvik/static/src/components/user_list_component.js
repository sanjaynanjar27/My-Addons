/** @odoo-module */

const { Component, useState, xml, useEffect, useSubEnv } = owl;
import UserInputComponent from './user_input_component';

class UserListComponent extends Component {
      static template = xml`
        <button class="btn btn-primary mb-3" t-on-click="addItemList">
            Add List
        </button>
        <div class="float-end">
          <t t-esc="state.parentState.totalItems" />/<t t-esc="totalBlocks" />
        </div>
        <div t-foreach="state.lists" t-as="list" t-key="list.id">
            <UserInputComponent t-props="{number:list.value, parentState: state.parentState}" />
            <hr />
        </div>
      `;

      setup() {
          this.state = useState({
              lists: [],
              value : 0,
              parentState: {
                  totalItems: 0, // Shared state for total items
              },
          });

        //   env.parentState = useState({
        // });

      }

      addItemList(event) {
        this.state.value ++;
        this.state.lists.push({
            id: Date.now(), // Unique ID for each block
            value: this.state.value
        });
        console.log("length>>>>>>>>111111>>>>>",this.state)
    }

    // get totalItems() {
    //     // Sum the items across all blocks
    //     console.log("this.state.lists>>>>>>>>>>>>>>>>>>>>",this.state.lists)
    //     return this.state.lists.reduce((sum, list) => {
    //         const child = this.refs[list.id];
    //         return sum + (child?.state.items.length || 0);
    //     }, 0);
    // }

    get totalBlocks() {
        return this.state.lists.length;
    }

}

UserListComponent.components = { UserInputComponent };
export default UserListComponent;