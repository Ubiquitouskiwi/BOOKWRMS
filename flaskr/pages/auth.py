import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.data_store.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', [user_id]
        ).fetchone()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        card_number = request.form['library_card_number']
        admin = request.form['is_admin']
        db = get_db()
        error = None

        if not first_name:
            error = 'Username is required.'
        elif not last_name:
            error = 'Password is required.'
        elif not card_number:
            error = 'All users require library card.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (first_name, last_name, library_card_number, is_admin) values (?, ?, ?, ?)',
                    (first_name, last_name, card_number, admin)
                )
                db.commit()
            except db.IntegrityError:
                error = f'{first_name} {last_name} is already registered'
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        card_number = None #request.form['library_card_number']
        db = get_db()
        error = None
        sql = None
        params = None
        
        if not first_name and not last_name and not card_number:            
            error = 'Must provide info to login.'
        elif not first_name and not last_name and card_number:
            sql = 'SELECT * FROM user WHERE library_card_number = ?'
            params = (card_number)
        elif not card_number and first_name and last_name:
            sql = 'SELECT * FROM user WHERE first_name = ? AND last_name = ?'
            params = (first_name, last_name)
        if sql is not None and params is not None:
            user = db.execute(
                sql, params
            ).fetchone()

        if user is None:
            error = 'No user found with that info.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')
            
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
