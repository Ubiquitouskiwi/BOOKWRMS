import datetime

from .base_object import BaseObject
from flaskr.data_store.db import get_db


class Checkout(BaseObject):
    def __init__(
        self,
        id=None,
        book_id=None,
        patron_name=None,
        checkout_date=None,
        checkout_duration=None,
        renew_count=None,
        checkin_date=None,
    ):
        self.id = id
        self.book_id = book_id
        self.patron_name = patron_name
        self.checkout_date = checkout_date
        self.checkout_duration = checkout_duration
        self.renew_count = renew_count
        self.checkin_date = checkin_date

        # Private fields
        self._db = None
        self._inflate_query_base = """
            SELECT
                *
            FROM
                checkout_log
            WHERE
                {0}
        """

    def save(self):
        # self._error_check()
        print("Saving checkout")
        today = datetime.datetime.today()
        if type(self.checkin_date) == type(""):
            self.checkin_date = datetime.datetime.strptime(
                self.checkin_date, "%Y-%M-%d"
            )
        diff = self.checkin_date - today
        checkout_duration = diff.days
        query = """
            INSERT INTO
                checkout_log (book_id, patron_name, checkout_duration, checkin_date, renew_count)
            VALUES
                (?, ?, ?, ?, ?)
        """
        query_params = [
            self.book_id,
            self.patron_name,
            checkout_duration,
            self.checkin_date,
            self.renew_count,
        ]

        self._check_db()
        self._db.execute(query, query_params)
        self._db.commit()
        print("Done Checking out")

    def inflate_by_id(self, id):
        where_clause = "id = ?"
        query = self._inflate_query_base.format(where_clause)
        query_params = [id]
        self._inflate(query, query_params)

    def _inflate(self, query, query_params):
        self._check_db()
        retrieved_checkout = self._db.execute(query, query_params).fetchone()
        self.id = retrieved_checkout["id"]
        self.book_id = retrieved_checkout["book_id"]
        self.checkout_date = retrieved_checkout["checkout_date"]
        self.checkout_duration = retrieved_checkout["checkout_duration"]
        self.checkin_date = retrieved_checkout["checkin_date"]
        self.renew_count = retrieved_checkout["renew_count"]

    def _check_db(self):
        if not self._db:
            self._db = get_db()

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
