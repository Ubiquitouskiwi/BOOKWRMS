from .base_object import BaseObject
from .author import Author
from flaskr.data_store.db import get_db

from datetime import timedelta, datetime

class Book(BaseObject):
    def __init__(self, book_id=None, title=None, isbn=None, author=None, cover_url=None, checkout_log=None):
        self.id = book_id
        self.title = title
        self.isbn = isbn
        self.cover_url = cover_url
        self.author = author
        self.checkout_log = checkout_log

        # Private fields
        self._db = None
        self._db_cursor = None
        self._inflate_query_base = """
            SELECT
                book.id,
                book.title,
                book.isbn,
                book.illustration_url,
                auth.first_name as author_first_name,
                auth.last_name as author_last_name,
                auth.olid as author_olid
            FROM
                book book
            LEFT JOIN
                author auth
            ON 
                book.author_id = auth.id
            WHERE 
                book.deleted = false
                AND {0}
        """

    def save(self):
        self._error_check()
        if not self.db:
            self.db = get_db()
        query = """
                INSERT INTO
                    book (title, author_id, isbn, illustration_url)
                VALUES
                    (?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE 
                    title = ?, author_id = ?, isbn = ?, illustration_url = ?
                """
        query_params = [
            self.title, 
            self.author_id, 
            self.isbn, 
            self.cover_url, 
            self.title, 
            self.author_id, 
            self.isbn, 
        self.cover_url]
        self.db.execute(query, query_params)
        self.db.commit()

    def inflate_by_id(self, id):
        where_clause = "book.id = ?"
        query = self._inflate_query_base.format(where_clause)
        query_params = [id]
        self._inflate(query, query_params)

    def inflate_by_isbn(self, isbn):
        where_clause = "book.isbn = ?"
        query = self._inflate_query_base.format(where_clause)
        query_params = [isbn]
        self._inflate(query, query_params)
    
    def inflate_by_title(self, title):
        where_clause = "book.title = ?"
        query = self._inflate_query_base.format(where_clause)
        query_params = [title]
        self._inflate(query, query_params)

    def _inflate(self, query, query_params):
        self._check_db()
        retrieved_book = self._db.execute(query, query_params).fetchone()

        self.id = retrieved_book['id']
        self.title = retrieved_book['title']
        self.isbn = retrieved_book['isbn']
        self.cover_url = retrieved_book['illustration_url']

        author = Author()
        author.first_name = retrieved_book['author_first_name']
        author.last_name = retrieved_book['author_last_name']
        author.olid = retrieved_book['author_olid']

        self.author = author
        self._inflate_checkout()

    def _inflate_checkout(self):
        self._check_db()
        checkout_log = []
        query = """
            SELECT
                u.first_name,
                u.last_name,
                u.library_card_number,
                cl.checkout_time,
                cl.checkout_duration
            FROM
                checkout_log cl
            LEFT JOIN
                user u
            ON
                cl.user_id = u.id 
            WHERE
                cl.deleted = 0
                AND cl.book_id = ?
        """
        query_params = [self.id]
        results = self._db.execute(query, query_params)
        for row in results:
            calc_return = timedelta(days=row['checkout_duration'])
            calc_return = row['checkout_time'] + calc_return
            returned = datetime.now() > calc_return
            checkout_log.append({
                'first_name': row['first_name'], 
                'last_name': row['last_name'], 
                'returned': returned, 
                'checkout_time': row['checkout_time'], 
                'expected_return': calc_return})
        self.checkout_log = checkout_log

    def _check_db(self):
        if not self._db:
            self._db = get_db()

    def _error_check(self):
        if type(self.id) is not type(int):
            raise TypeError(f"Book ID can not be {type(self.id)}, must be int. Check book table in DB.")
        if type(self.title) is not type(str):
            raise TypeError(f"Book title can not be {type(self.title)}, must be str")
        if type(self.isbn) is not type(int):
            raise TypeError(f"Book ISBN can not be {type(self.isbn)}, must be int.")
        if type(self.author_id) is not type(int):
            raise TypeError(f"Book author_id can not be {type(self.author_id)}, must be int")
        if type(self.cover_url) is not type(str):
            raise TypeError(f"Book cover_url can not be {type(self.cover_url)}, must be str")
        
    def __str__(self):
        return f"{self.title}"