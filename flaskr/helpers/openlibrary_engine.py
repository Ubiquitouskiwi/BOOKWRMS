from olclient.openlibrary import OpenLibrary
import olclient.common as common

import pprint

class OpenLibraryClient():
    def __init__(self):
        self.client = OpenLibrary()

    def search_isbn(self, isbn):
        return_value = None
        edition = self.client.Edition.get(isbn=isbn)
        if edition is not None:
            return_value = self.client.Work.get(edition.work_olid)
        else:
            return_value = edition
        return return_value

# pp = pprint.PrettyPrinter()  
# ol = OpenLibraryClient()
# pp.pprint(ol.search_isbn(9780062502179))