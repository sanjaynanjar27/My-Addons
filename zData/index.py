"""
Odoo's **QWeb** is a powerful XML-based templating engine primarily used for rendering views and reports. In QWeb templates, various XML attributes and directives control the rendering logic and structure of the content. Here’s a rundown of commonly used attributes and directives in Odoo QWeb templates, focusing on making dynamic views and reports in Odoo.

### Common QWeb Template Attributes




### Structuring QWeb Templates for Dynamic Views and Reports

#### Basic Example of a Report with QWeb

Here’s a sample template for a sales report:

```xml
<template id="report_saleorder">
    <t t-call="web.external_layout">
        <div class="page">
            <h2>Sales Order Report</h2>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <t t-foreach="doc.order_line" t-as="line">
                        <tr>
                            <td><t t-esc="line.product_id.name"/></td>
                            <td><t t-esc="line.product_uom_qty"/></td>
                            <td><t t-esc="line.price_unit"/></td>
                            <td><t t-esc="line.price_total"/></td>
                        </tr>
                    </t>
                </tbody>
            </table>
        </div>
    </t>
</template>
```

#### Tips for Dynamic Content in QWeb

- **Reuse Components**: Use `t-call` to include common headers, footers, or custom components across templates.
- **Variable Management**: Use `t-set` to define variables for data or reusable content sections.
- **Conditional Rendering**: Use `t-if`, `t-else`, and `t-elif` to conditionally display information based on context.
- **Dynamic Styling**: Use `t-att` or `t-attf` for setting classes, styles, or any HTML attributes dynamically.

### Example of a Custom QWeb View

For a detailed view, such as an employee profile, a QWeb template could look like this:

```xml
<template id="employee_profile_template">
    <t t-call="web.external_layout">
        <div class="page">
            <div t-if="employee.photo">
                <img t-att-src="'data:image/png;base64,%s' % employee.photo" alt="Employee Photo"/>
            </div>
            <h3><t t-esc="employee.name"/></h3>
            <p><strong>Position:</strong> <t t-esc="employee.position_id.name"/></p>
            <p><strong>Department:</strong> <t t-esc="employee.department_id.name"/></p>
            <p><strong>Email:</strong> <t t-esc="employee.work_email"/></p>
        </div>
    </t>
</template>
```

This example displays an employee’s details with dynamic checks and image rendering, illustrating QWeb's flexibility for creating interactive, data-driven layouts.

"""
