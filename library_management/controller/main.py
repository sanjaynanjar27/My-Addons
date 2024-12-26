import json
import logging

from odoo.exceptions import UserError
from odoo.http import request

from odoo import http

_logger = logging.getLogger(__name__)


class LibController(http.Controller):

    @http.route('/library', website=True, type="http", auth="public", methods=['GET'])
    def get_library(self, **args):
        # Fetch all books
        books = request.env['library.books'].sudo().search([])
        for i in books:
            print(f"{i.name}  Field Created By , {i.create_uid.name}")
        data = {'books': books}
        return request.render('library_management.books_data_template', data)

    @http.route('/library/open_form', website=True, type='http', auth='public')
    def open_form(self):
        authors = request.env['book.authors'].sudo().search([])
        categories = request.env['book.category'].sudo().search([])

        return request.render("library_management.books_csrf_token_form",
                              {'authors': authors, 'categories': categories})

    @http.route('/library/success', website=True, type="http", auth="public")
    def success_page(self):
        image_url = '/library_management/static/src/img/images.png'
        return request.render("library_management.success_template", {'img': image_url})

    @http.route('/library/form/', type="http", auth="public", methods=['POST'], csrf=True, website=True)
    def submit_form(self, **args):
        name = args.get('name')
        avail = args.get('avail') == 'on'
        author_id = int(args.get('author', 0))
        category_ids = list(map(int, args.get('category', []).split(',')))

        if not name or not author_id:
            raise UserError("Both book name and author are required.")

        author = request.env['book.authors'].sudo().browse(author_id)
        if not author:
            raise UserError(f"Author with ID {author_id} not found.")

        categories = request.env['book.category'].sudo().browse(category_ids)
        if not categories:
            raise UserError("At least one valid category is required.")

        request.env['library.books'].sudo().create({'name': name, 'avail': avail, 'author': author.id,
                                                    'category': [(6, 0, [category.id for category in categories])]})

        return request.redirect('/library/success')

    @http.route('/library/json/get_books', type='http', auth='public', methods=['GET'], cors="*")
    def get_books_json(self, **args):
        # Fetch all books
        books = request.env['library.books'].sudo().search([])

        # Prepare the list of books in JSON format
        books_data = [{'id': book.id, 'name': book.name, 'avail': book.avail, 'author': book.author.name,
                       'create_uid': book.create_uid.name,
                       'create_date': book.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                       'write_date': book.write_date.strftime('%Y-%m-%d %H:%M:%S'),
                       'categories': [category.name for category in book.category]} for book in books]
        return json.dumps({'status': 'success', 'books': books_data})
