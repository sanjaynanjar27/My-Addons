from odoo import http
from odoo.http import request
from io import BytesIO
import xlsxwriter
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ProjectTaskReportController(http.Controller):

    @http.route('/filter_products', auth='public', website=True)
    def filter_products(self, category_id=None):
        # Get categories
        categories = request.env['product.category'].sudo().search([])
        print(category_id)
        domain = []
        if category_id:
            domain = [('categ_id', '=', int(category_id))]
        products = request.env['product.product'].sudo().search(domain)

        return request.render('project_custom.product_listing_template_2', {
            'products': products,
            'categories': categories
        })

    @http.route('/search_filter', auth='public',website=True)
    def search_filter(self,**kwargs):
        search_query = kwargs.get('name_search')
        print(search_query)
        products = request.env['product.product'].sudo().search([('name', 'ilike', search_query)])
        return request.render('project_custom.product_listing_template_2', {
            'products': products,
        })

    @http.route('/product_product', auth='public', website=True)
    def fetch_data_from_product_product(self):
        all_categ = request.env['product.category'].sudo().search([])
        products = request.env['product.product'].sudo().search([])
        return request.render('project_custom.product_listing_template_2', {
            'products': products,
            'categories': all_categ,
        })

    @http.route('/product_detail/<int:product_id>', auth='public', website=True)
    def product_detail(self, product_id, **kw):
        product = request.env['product.product'].sudo().browse(product_id)
        all_categ = request.env['product.category'].sudo().search([])
        print(all_categ)
        categories = product.categ_id
        categories_name = product.categ_id.name

        print(categories , categories_name)

        if not product.exists():
            return request.render('website.404')

        return request.render('project_custom.product_detail_template', {
            'product': product
        })

    @http.route('/product_listing', type='http', auth="public", website=True)
    def product_listing(self, **kwargs):
        search_query = kwargs.get('search_query', '').strip()
        category_filter = kwargs.get('category_filter', '')
        price_filter = kwargs.get('price_filter', '')

        # Build the domain for product search and filtering
        domain = []
        if search_query:
            domain.append(('name', 'ilike', search_query))
        if category_filter:
            domain.append(('categ_id.name', '=', category_filter))
        if price_filter == '1':
            domain.append(('lst_price', '<', 50))
        elif price_filter == '2':
            domain.append(('lst_price', '>=', 50), ('lst_price', '<=', 200))
        elif price_filter == '3':
            domain.append(('lst_price', '>', 200))

        # Fetch filtered products
        products = request.env['product.product'].sudo().search(domain)

        return request.render('project_custom.product_listing_template_2', {
            'products': products,
        })

    @http.route('/delivery/product_review', auth='public', website=True)
    def web_page_to_review_products(self, picking_id=None):
        picking = request.env['stock.picking'].sudo().browse(int(picking_id)) if picking_id else None
        delivery_items = []
        if picking:
            for move_line in picking.move_line_ids:
                move = move_line.move_id

                product_id = move.product_id.id
                product_name = move.product_id.name
                product_uom = move.product_uom.name
                product_description = move.product_id.description_sale or "No description available"
                product_image_url = f"/web/image/product.product/{product_id}/image_1024"

                delivery_items.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'uom': product_uom,
                    'description': product_description,
                    'image_url': product_image_url,
                })

        # Render the review page template and pass the delivery items
        return request.render('project_custom.web_review_template', {
            'delivery_items': delivery_items,
            'picking': picking
        })

    @http.route('/submit/review', type='http', auth="public", methods=['POST'], csrf=True, website=True)
    def submit_review(self, **kwargs):
        rating = kwargs.get('rating', 0)  # Assuming you pass rating explicitly
        review_description = kwargs.get('review_description', '')
        product_id = kwargs.get('product_id')

        _logger.info(f"Rating: {rating}")
        _logger.info(f"Review Description: {review_description}")
        _logger.info(f"Product ID: {product_id}")

        if product_id:
            request.env['product.review'].sudo().create({
                'product_id': product_id,  # Assuming the product has a variant
                'ratings': rating,  # Rating
                'description': review_description,  # Review description
            })
        return request.redirect('/contactus-thank-you')

    @http.route('/crm_lead', auth='public', website=True)
    def web_form(self, **kwargs):
        partner_ids = request.env['res.partner'].sudo().search([])
        print(f"These are partners : {partner_ids}")
        return request.render('project_custom.web_form_template', {'partner_ids': partner_ids})

    @http.route('/crm/crm_lead_form/', type='http', auth='public', methods=['POST'], csrf=True, website=True)
    def submit_form(self, **args):
        name = args.get('name')
        partner_id = args.get('partner_ids')
        email_from = args.get('email')
        phone = args.get('phone')
        probability = args.get('probability')
        expected_revenue = args.get('expected_revenue')
        _logger.info(
            f"NAME : {name}, EMAIL : {email_from}, PROBABILITY : {probability},Partner ID :  {partner_id},Phone : {phone}")
        name = name + "'s Lead"
        result = request.env['crm.lead'].sudo().create({
            'name': name,
            'partner_id': partner_id,
            'email_from': email_from,
            'phone': phone,
            'probability': probability,
            'expected_revenue': expected_revenue
        })
        if result:
            return request.redirect('/contactus-thank-you')
        else:
            UserError("Data Not Submitted")

    @http.route('/project/task/report/xlsx', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_xlsx_report(self, **kwargs):
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        if not start_date or not end_date:
            return "Please provide start and end dates."

        task_ids = request.env['project.task'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date)
        ])

        task_info = []
        for task in task_ids:
            user_info = {
                'name': task.user_id.name if task.user_id else "No User ID Found"
            }
            company_info = {
                'name': task.company_id.name if task.company_id else "No Company ID Found",
                'email': task.company_id.email if task.company_id else "No Email Found",
                'phone': task.company_id.phone if task.company_id else "No Phone Found",
            }

            project_info = {
                'company_id': task.project_id.company_id.name if task.project_id and task.project_id.company_id else "No Company ID Found",
                'date_start': task.project_id.date_start if task.project_id and task.project_id.date_start else "No Start Date",
                'date': task.project_id.date if task.project_id and task.project_id.date else "No Date",
                'description': task.project_id.description if task.project_id and task.project_id.description else "No Description",
                'team_name': task.project_id.team_name if hasattr(task.project_id,
                                                                  'team_name') and task.project_id.team_name else "No Team Name",
            }

            task_info.append({
                'name': task.name,
                'user_id': user_info,
                'company_id': company_info,
                'project_info': project_info,
            })

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Task Report')

        header_format = workbook.add_format(
            {'bold': True, 'bg_color': '#D3D3D3', 'align': 'center', 'valign': 'vcenter'})

        worksheet.write('A1', 'Task Name', header_format)
        worksheet.write('B1', 'User', header_format)
        worksheet.write('C1', 'Company', header_format)
        worksheet.write('D1', 'Email', header_format)
        worksheet.write('E1', 'Phone', header_format)
        worksheet.write('F1', 'Project', header_format)
        worksheet.write('G1', 'Start Date', header_format)
        worksheet.write('H1', 'Project Date', header_format)
        worksheet.write('I1', 'Description', header_format)
        worksheet.write('J1', 'Team Name', header_format)

        row = 1
        for task in task_info:
            worksheet.write(row, 0, task['name'])
            worksheet.write(row, 1, task['user_id']['name'])
            worksheet.write(row, 2, task['company_id']['name'])
            worksheet.write(row, 3, task['company_id']['email'])
            worksheet.write(row, 4, task['company_id']['phone'])
            worksheet.write(row, 5, task['project_info']['company_id'])
            worksheet.write(row, 6, task['project_info']['date_start'])
            worksheet.write(row, 7, task['project_info']['date'])
            worksheet.write(row, 8, task['project_info']['description'])
            worksheet.write(row, 9, task['project_info']['team_name'])
            row += 1

        workbook.close()
        output.seek(0)

        response = request.make_response(
            output.read(),
            headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                     ('Content-Disposition', 'attachment; filename="task_report.xlsx"')]
        )

        return response
