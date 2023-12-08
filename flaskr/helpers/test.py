from openlibrary_engine import OpenLibraryClient
import pprint


def main():
    isbn = 267381166890
    client = OpenLibraryClient()
    resp = client.search_isbn(isbn)
    cover = f"TEST TEST TEST testt tetstststststststststtststststsstasgdgadg adg agd {resp}  afgasg adg adg ad ga dg ag ag sdgsafhadgadg adg adg adg adg adg "
    print(cover)


if __name__ == "__main__":
    main()
