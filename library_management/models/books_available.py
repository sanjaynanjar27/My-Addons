import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class BooksAvailable(models.Model):
    _name = 'library.books'
    _description = 'Available Books'
    _rec_names_search = ['name', 'author']

    name = fields.Char(string="Book Name")
    avail = fields.Boolean(string="Is Available?")
    author = fields.Many2one('book.authors', string="Authors")
    author_name = fields.Char(related='author.name', string="Name from Relation")
    category = fields.Many2many('book.category', string="Book Category")

    @api.model
    def create(self, vals):
        _logger.info("Odoo ORM Method For Creating Value: %s", vals)
        return super(BooksAvailable, self).create(vals)

    def write(self, vals):
        _logger.info("Values Update: %s", vals)
        return super(BooksAvailable, self).write(vals)

    @api.onchange('name')
    def print_hello(self):
        print("Hello On Change")

    def action_print_report(self):
        data = {'id': self.id}

        book = self.env['library.books'].browse(self.id)

        return self.env.ref('library_management.books_report_template').report_action(self, data=data)




class Author(models.Model):
    _name = 'book.authors'
    _description = 'All list about authors in database'
    name = fields.Char(string="Author")

    # @api.model  # def get (self, vals) :  #     return super (Author, self).create (vals)


class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Select Book Category'
    name = fields.Char(string="Book Category")
    author_name = fields.Char(string="Author Name")

    @api.model
    def create(self, vals):
        _logger.info("Objects You Enter In your Fields : %s", vals)
        book = super(BookCategory, self).create(vals)
        authors = self.env['book.authors'].create({'name': book.author_name})
        author_name_db = authors['name']
        if book.author_name == author_name_db:
            _logger.info("Authors Exists: %s", authors['name'])
        else:
            self.env['book.authors'].create({'name': book.author_name})
            _logger.info("Author Created : %s", authors['name'])
        return book


class BooksPDFReport(models.TransientModel):
    _name = 'library.management.report'
    _description = 'Books Form'

    book_id = fields.Many2one('library.books', string="Book Name")
    author_name = fields.Char(related="book_id.author_name", string="Author Name")
