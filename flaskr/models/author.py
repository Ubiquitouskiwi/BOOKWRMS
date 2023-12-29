from .base_object import BaseObject
from flaskr.data_store.db import get_db


class Author(BaseObject):
    def __init__(
        self,
        author_id=None,
        first_name=None,
        middle_name=None,
        last_name=None,
        olid=None,
    ):
        self.id = author_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.olid = olid

        # Private fields
        self._write_db = None
        self._read_db = None
        self._inflate_query_base = """
            SELECT
                *
            FROM
                author
            WHERE
                {0}
        """

    def save(self):
        # self._error_check()

        query = """
            INSERT INTO
                author (first_name, middle_name, last_name, olid)
            VALUES
                (%s, %s, %s, %s)
        """
        query_params = [self.first_name, self.middle_name, self.last_name, self.olid]

        self._check_db("write")
        self._write_db_cursor.execute(query, query_params)
        self._write_db.commit()
        self._write_db_cursor.close()

    def inflate_by_name(self, first_name, last_name):
        where_clause = "first_name = %s AND last_name = %s"
        query = self._inflate_query_base.format(where_clause)
        query_params = [first_name, last_name]
        self._inflate(query, query_params)

    def inflate_by_olid(self, author_olid):
        where_clause = "olid = %s"
        query = self._inflate_query_base.format(where_clause)
        query_params = author_olid
        print(query)
        print(query_params)
        self._inflate(query, [query_params])

    def _inflate(self, query, query_params):
        self._check_db("read")
        self._db_read_cursor.execute(query, query_params)
        retrieved_author = self._db_read_cursor.fetchone()
        self.id = retrieved_author["id"]
        self.first_name = retrieved_author["first_name"]
        self.last_name = retrieved_author["last_name"]
        self.olid = retrieved_author["olid"]

    def _check_db(self, conn_type="read"):
        if conn_type == "read":
            if not self._read_db:
                self._read_db = get_db()
                self._db_read_cursor = self._read_db.cursor()
        elif conn_type == "write":
            if not self._write_db:
                self._write_db = get_db("write")
                self._write_db_cursor = self._write_db.cursor()

    def _error_check(self):
        if type(self.first_name) is not type(str):
            raise TypeError(
                f"Author first_name can not be {type(self.first_name)}, must be str"
            )
        if type(self.last_name) is not type(str):
            raise TypeError(
                f"Author last_name can not be {type(self.last_name)}, must be str"
            )
        if type(self.olid) is not type(str):
            raise TypeError(f"Author OLID can not be {type(self.olid)}, must be str")

    # def __del__(self):
    #     if self._db:
    #         self._db.close()

    def __str__(self):
        return f"First: {self.first_name}, Last: {self.last_name}, OLID: {self.olid}"
