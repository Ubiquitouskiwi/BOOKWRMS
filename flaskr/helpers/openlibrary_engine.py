from olclient import OpenLibrary
import olclient.common as common

# from ..data_store.db import get_db

import pprint


class OpenLibraryClient:
    def __init__(self):
        self.client = OpenLibrary()
        # self.db = get_db()

    def search_isbn(self, isbn):
        return_value = None
        edition = self.client.Edition.get(isbn=isbn)
        if edition is not None:
            return_value = self.client.Work.get(edition.work_olid)
        else:
            return_value = edition
        return return_value

    def get_author(self, olid):
        author = self.client.Author.get(olid=olid)
        return author

    def get_author_from_work(self, work):
        author = work.authors[0]
        if author is not None:
            author_path = author["author"]["key"]
            author_olid = author_path.split("/")[-1]
            author = self.get_author(author_olid)

        return author

    def _check_db(self, first_name, last_name):
        return self.db.execute(
            "SELECT * FROM authors WHERE first_name = ? AND last_name = ?",
            (first_name, last_name),
        )


# pp = pprint.PrettyPrinter()
# ol = OpenLibraryClient()
# work = ol.search_isbn(9780062502179)
# author = ol.get_author_from_work(work)
# print(author)
