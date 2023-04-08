from .base_object import BaseObject
from flaskr.data_store.db import get_db

class Author(BaseObject):
    def __init__(self, author_id=None, first_name=None, last_name=None, olid=None):
        self.id = author_id
        self.first_name = first_name
        self.last_name = last_name
        self.olid = olid

        # Private fields
        self._db = None
        self._inflate_query_base = """
            SELECT
                *
            FROM
                authors
            WHERE
                {0}
        """

    def save(self):
        self._error_check()

        query = """
            INSERT INTO
                authors (first_name, last_name, olid)
            VALUES
                (?, ?, ?)
            ON DUPLICATE KEY UPDATE 
                first_name = ?, last_name = ?, olid = ?
        """
        query_params = [self.first_name, self.last_name, self.olid, self.first_name, self.last_name, self.olid]

        self._check_db()
        self.db.execute(query, query_params)
        self.db.commit()
        
    def inflate_by_name(self, first_name, last_name):
        where_clause = "first_name = ? AND last_name = ?"
        query = self._inflate_query_base.format(where_clause)
        query_params = [first_name, last_name]
        self._inflate(query, query_params)

    def inflate_by_olid(self, author_olid):
        where_clause = "olid = ?"
        query = self._inflate_query_base.format(where_clause)
        query_params = (author_olid)        
        self._inflate[query, query_params]      

    def _inflate(self, query, query_params):
        self._check_db()
        retrieved_author = self._db.execute(query, query_params).fetchone()
        self.id = retrieved_author.get('id')
        self.first_name = retrieved_author.get('first_name')
        self.last_name = retrieved_author.get('last_name')
        self.olid = retrieved_author.get('olid')

    def _check_db(self):
        if not self._db:
            self._db = get_db()

    def _error_check(self):
        if type(self.first_name) is not type(str):
            raise TypeError(f"Author first_name can not be {type(self.first_name)}, must be str")
        if type(self.last_name) is not type(str):
            raise TypeError(f"Author last_name can not be {type(self.last_name)}, must be str")
        if type(self.olid) is not type(str):
            raise TypeError(f"Author OLID can not be {type(self.olid)}, must be str")
        
    def __del__(self):
        if self.db:
            self.db.close()
    
    def __str__(self):
        return f"First: {self.first_name}, Last: {self.last_name}, OLID: {self.olid}"