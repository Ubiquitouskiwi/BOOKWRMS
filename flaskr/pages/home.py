from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.pages.auth import login_required
from flaskr.data_store.db import get_db

bp = Blueprint('home', __name__)

def get_book(id):
    book = get_db().execute(
        '''
        SELECT 
                book.id, 
                book.title, 
                book.isbn, 
                book.illustration_url,
                author.first_name,
                author.last_name
            FROM
                books book
            JOIN
                authors author
            ON 
                book.author_id = author.id
            WHERE
                book.id = ?
        ''', [id]
    ).fetchone()

    if book is None:
        abort(404, f'Book id {id} does not exist.')
    
    return book

@bp.route('/')
def index():
    db = get_db()
    books = db.execute(
        '''
            SELECT 
                book.id as id, 
                book.title as title, 
                book.isbn as isbn, 
                book.illustration_url as illustration_url,
                author.first_name as first_name,
                author.last_name as last_name
            FROM
                books book
            JOIN
                authors author
            ON 
                book.author_id = author.id
            WHERE
                book.deleted = FALSE
                AND author.deleted = FALSE
        '''
    ).fetchall()
    return render_template('home/index.html', books=books)

@bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        illustration_url = request.form['illustration_url']
        author_id = 1
        error = None

        if not title:
            error = 'Title is a required field.'
        elif not isbn:
            error = 'ISBN is a required field.'
        elif not illustration_url:
            error = 'Illustration_url is a required field.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO books (title, author_id, isbn, illustration_url) VALUES (?, ?, ?, ?)',
                (title, author_id, isbn, illustration_url)
            )
            db.commit()
            return redirect(url_for('home.index'))
    
    return render_template('home/add_book.html')

@bp.route('/<int:id>/edit_book', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = get_book(id)

    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        cover_url = request.form['illustration_url']
        error = None

        if not title:
            error = 'Title is a required field.'
        elif not isbn:
            error = 'ISBN is a required field.'
        elif not cover_url:
            error = 'Book cover URL is a required field.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE books SET title = ?, isbn = ?, illustration_url = ? WHERE id = ?',
                (title, isbn, cover_url, id)
            )
            db.commit()
            return redirect(url_for('home.index'))
    return render_template('home/edit_book.html', book=book)
    
@bp.route('/<int:id>/delete_book', methods=['POST'])
@login_required
def delete_book(id):
    book = get_book(id)
    
    if book is not None:
        db = get_db()
        db.execute(
            'UPDATE books SET deleted = TRUE WHERE id = ?',
            [id]
        )
        db.commit()
        return redirect(url_for('home.index'))
    
@bp.route('/<int:id>/book_details', methods=[ 'GET'])
def book_details(id):
    book = get_book(id)
    error = None

    if book is None:
        error = 'Book ID not found'

    return render_template('home/book_details.html', book=book)