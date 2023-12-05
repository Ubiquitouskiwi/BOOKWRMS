from openlibrary_engine import OpenLibraryClient


def main():
    isbn = 9781526617163
    client = OpenLibraryClient()
    resp = client.search_isbn(isbn)
    author = client.get_author_from_work(resp)
    print(author.olid)


if __name__ == "__main__":
    main()
