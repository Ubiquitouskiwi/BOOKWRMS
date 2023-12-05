from openlibrary_engine import OpenLibraryClient
import pprint


def main():
    isbn = 9780451166890
    client = OpenLibraryClient()
    resp = client.search_isbn(isbn)
    author = client.get_author_from_work(resp)
    pp = pprint.PrettyPrinter(width=41, compact=True)
    pp.pprint(author.links)


if __name__ == "__main__":
    main()
