from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
    session,
)
from werkzeug.exceptions import abort

from flaskr.pages.auth import login_required
from flaskr.models.book import Book
from flaskr.models.author import Author
from flaskr.models.checkout import Checkout
from flaskr.data_store.db import get_db
from ..helpers.openlibrary_engine import OpenLibraryClient

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    db = get_db()
    books = db.execute(
        """
            SELECT 
                book.id as id, 
                book.title as title, 
                book.isbn as isbn, 
                book.illustration_url as illustration_url,
                author.first_name as first_name,
                author.last_name as last_name
            FROM
                book book
            JOIN
                author author
            ON 
                book.author_id = author.id
            WHERE
                book.deleted = FALSE
                AND author.deleted = FALSE
        """
    ).fetchall()
    return render_template("home/index.html", books=books)


@bp.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        isbn = request.form["isbn"]
        error = None
        current_app.logger.info("Post Received")

        if not isbn:
            error = "ISBN or title must not be blank."
            current_app.logger.info("Title and isbn blank")

        if error is not None:
            current_app.logger.info("Error found")
            flash(error)
        else:
            ol_client = OpenLibraryClient()
            current_app.logger.info("No errors found")
            if isbn:
                current_app.logger.info("ISBN is not blank")
                book_resp = ol_client.search_isbn(isbn)
                author_resp = ol_client.get_author_from_work(book_resp)
                cover = f"https://covers.openlibrary.org/b/id/{book_resp.covers[0]}.jpg"
                author_name_split = author_resp.name.split(" ")
                first_name = author_name_split[0]
                last_name = author_name_split[-1]
                middle_name = None
                if len(author_name_split) == 3:
                    middle_name = author_name_split[1]
                author = Author(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    olid=author_resp.olid,
                )
                author.save()
                author = Author()
                author.inflate_by_name(
                    author_resp.name.split(" ")[0], author_resp.name.split(" ")[-1]
                )
                book = Book(
                    title=book_resp.title,
                    isbn=isbn,
                    cover_url=cover,
                    author_id=author.id,
                )
                book.save()

        return redirect(url_for("home.index"))

    return render_template("home/add_book.html")


@bp.route("/<int:id>/edit_book", methods=["GET", "POST"])
@login_required
def edit_book(id):
    book = Book()
    book.inflate_by_id(id)

    if request.method == "POST":
        title = request.form["title"]
        isbn = request.form["isbn"]
        cover_url = request.form["illustration_url"]
        error = None

        if not title:
            error = "Title is a required field."
        elif not isbn:
            error = "ISBN is a required field."
        elif not cover_url:
            error = "Book cover URL is a required field."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE book SET title = ?, isbn = ?, illustration_url = ? WHERE id = ?",
                (title, isbn, cover_url, id),
            )
            db.commit()
            return redirect(url_for("home.index"))
    return render_template("home/edit_book.html", book=book)


@bp.route("/<int:id>/delete_book", methods=["POST"])
@login_required
def delete_book(id):
    book = Book()
    book.inflate_by_id(id)

    if book.id is not None:
        db = get_db()
        db.execute("UPDATE book SET deleted = TRUE WHERE id = ?", [id])
        db.commit()
        return redirect(url_for("home.index"))


@bp.route("/<int:id>/checkout_book", methods=["GET", "POST"])
@login_required
def checkout_book(id):
    if request.method == "POST":
        book = Book()
        book.inflate_by_id(id)

        if book.id is not None:
            checkout = Checkout()
        return redirect(url_for("home.index"))
    return render_template("home/checkout_book.html")


@bp.route("/<int:id>/book_details", methods=["GET"])
def book_details(id):
    book = Book()
    book.inflate_by_id(id)
    client = OpenLibraryClient()

    book_resp = client.search_isbn(book.isbn)
    author_resp = client.get_author_from_work(book_resp)

    try:
        book.author_links = author_resp.links
    except AttributeError:
        current_app.logger.info(f"Links not found for {book.author_id}")
    book.summary = book_resp.description

    return render_template("home/book_details.html", book=book)
