from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

##
#Neišbaigtos temos dėl laiko stokos:
#1) @api.depens
#2) compute
#3) Action'ai
#4) Group'ų panaudojimas
#5) Controller'iai
#6) Report'ai 
#7) Testing
#8) Loginimas
##

class EfLibraryBook(models.Model):
    _name = 'ef.library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    short_description = fields.Char(string='Short description')
    page_count = fields.Integer(string='Page count')
    genre = fields.Char(string='Genre (can be more than one)')
    borrowings_ids = fields.One2many('ef.library.book.borrowing', 'ref_book_id', string='Borrowings')

class EfLibraryBookBorrowing(models.Model):
    _name = 'ef.library.book.borrowing'
    _description = 'Book Borrowing'

    ref_book_id = fields.Many2one('ef.library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.today(), required=True)
    to_return_date = fields.Date(string='To return Date', required=True)
    #Panaudota selection, tik ar ne geriau būtų kurti kaip atskirą esybę(lentelę) klasifikatoriams?
    borrow_state = fields.Selection([
        ('R', 'Reserved'),
        ('B', 'Borrowed'),
        ('RB', 'Returned back'),
        ('C', 'Canceled'),
        ], 'Borrowed books state', required=True)
        
    @api.model
    def _check_return_dates(self):
        # Rasti knygas, kurioms suėjo grąžinimo terminas
        overdue_borrowings = self.search([('to_return_date', '<', fields.Date.today()), ('borrow_state', '=', 'R'), ('borrow_state', '=', 'B')])

        # Siųsti pranešimą
        for borrowing in overdue_borrowings:
            borrower = borrowing.borrower_id
            if borrower and borrower.email:
                subject = _('Overdue Book Return Reminder')
                body = _('Dear %s,\n\nThis is a reminder that you have an overdue book to return.\n\nBook: %s\nReturn Date: %s\n\nPlease return the book as soon as possible.') % (
                    borrower.name, borrowing.book_id.name, borrowing.to_return_date
                )

                try:
                    # Siunčiame
                    borrower.message_post(
                        subject=subject,
                        body=body,
                        subtype_id=self.env.ref('mail.mt_comment').id,
                        partner_ids=[borrower.id],
                    )
                except ValidationError as e:
                    # Blogai
                    pass