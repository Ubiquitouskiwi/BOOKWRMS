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
from datetime import datetime

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
    tags = {}
    for book in books:
        tags[book["id"]] = []
        fetched_tags = db.execute(
            """
            SELECT
                id,
                tag_value,
                tag_color
            FROM
                user_book_tag
            WHERE
                deleted = FALSE
                AND book_id = ?
            """,
            [book["id"]],
        ).fetchall()
        tags[book["id"]] = fetched_tags
    return render_template("home/index.html", books=books, tags=tags)


@bp.route("/tag/<int:id>/delete-tag", methods=["GET"])
@login_required
def delete_tag(id):
    db = get_db()

    db.execute(
        """
        DELETE FROM
            user_book_tag
        WHERE
            id = ?
        """,
        [id],
    )
    db.commit()

    return redirect(request.referrer)


@bp.route("/add-tag", methods=["POST"])
@login_required
def add_tag():
    tag_value = request.form["tag_value"]
    tag_color = request.form["tag_color"]
    book_id = request.form["modal_book_id"]
    error = None

    if not tag_value:
        error = "Must supply tag value."
    if not tag_color:
        error = "Must supply tag color."

    if error is None:
        tag_color = tag_color.upper().strip("#")
        db = get_db()
        db.execute(
            """
            INSERT INTO
                user_book_tag (book_id, user_id, tag_value, tag_color)
            VALUES
                (?, ?, ?, ?)            
            """,
            [book_id, 1, tag_value, tag_color],
        )
        db.commit()
        redirect
    else:
        flash(error)
    return redirect(request.referrer)


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
                book_resp = ol_client.search_isbn(isbn)
                if book_resp is not None:
                    author_resp = ol_client.get_author_from_work(book_resp)
                    try:
                        cover = f"https://covers.openlibrary.org/b/id/{book_resp.covers[0]}.jpg"
                    except AttributeError:
                        cover = "https://www.mobileread.com/forums/attachment.php?attachmentid=111284&d=1378756884"
                    author_name_split = author_resp.name.split(" ")
                    first_name = author_name_split[0]
                    if len(author_name_split) > 1:
                        last_name = author_name_split[1]
                    author = Author(
                        first_name=first_name,
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
                else:
                    flash(f"ISBN: {isbn} is not a valid barcode.")

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


@bp.route("/<int:id>/return_book", methods=["GET"])
@login_required
def return_book(id):
    db = get_db()
    db.execute(
        """
        UPDATE 
            checkout_log
        SET
            returned = True
        WHERE
            book_id = ?
    """,
        [id],
    )
    db.commit()

    return redirect(url_for("home.index"))


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
        patron_name = request.form["patron-name"]
        checkin_date = request.form["checkin-date"]
        print(checkin_date)
        checkin_date = datetime.strptime(checkin_date, "%Y-%m-%d")
        print(checkin_date)
        error = None

        if not checkin_date:
            error = "Checkin Date cannot be empty"
        elif not patron_name:
            error = "Patron name cannot be empty"
        elif checkin_date <= datetime.today():
            error = "Checkin Date must be later than today."

        if error is None:
            print("No error")
            book = Book()
            book.inflate_by_id(id)

            if book.id is not None:
                print("ID is not none")
                checkout = Checkout()
                checkout.book_id = id
                checkout.patron_name = patron_name
                checkout.checkin_date = checkin_date
                checkout.renew_count = 0
                checkout.save()
                print("Saved book")

            return redirect(url_for("home.index"))
        else:
            flash(error)
    return render_template("home/checkout_book.html")


@bp.route("/<int:id>/book_details", methods=["GET"])
def book_details(id):
    book = Book()
    book.inflate_by_id(id)
    client = OpenLibraryClient()

    book_resp = client.search_isbn(book.isbn)
    author_resp = client.get_author_from_work(book_resp)

    db = get_db()

    fetched_tags = db.execute(
        """
            SELECT
                id,
                tag_value,
                tag_color
            FROM
                user_book_tag
            WHERE
                deleted = FALSE
                AND book_id = ?
            """,
        [id],
    ).fetchall()

    try:
        book.author_links = author_resp.links
    except AttributeError:
        current_app.logger.info(f"Links not found for {book.author_id}")
    book.summary = book_resp.description

    return render_template("home/book_details.html", book=book, tags=fetched_tags)


@bp.route("/search_book", methods=["POST"])
def search_book():
    search_type = request.form["search_type"]
    search_criteria = request.form["search_criteria"]
    if search_criteria != "":
        db = get_db()
        print("search")
        if search_type == "isbn":
            try:
                print("isbn search")
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
                        AND isbn = ?
                """,
                    [int(search_criteria)],
                ).fetchall()
                return render_template("home/index.html", books=books)
            except ValueError:
                error = f"{search_criteria} is not a ISBN."
                flash(error)
        elif search_type == "title":
            print("title search")
            criteria_split = search_criteria.split(" ")
            where_clause = " AND ("
            for index, word in enumerate(criteria_split):
                if index > 0:
                    where_clause += " OR "
                where_clause += f' book.title LIKE "%{word}%" '
            sql = (
                """SELECT 
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
                AND author.deleted = FALSE"""
                + where_clause
                + ")"
            )
            print(sql)
            books = db.execute(sql).fetchall()
            print(books)
            return render_template("home/index.html", books=books)

    return redirect(url_for("home.index"))
