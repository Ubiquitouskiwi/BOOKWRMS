from flask import Blueprint, render_template, Response, redirect, url_for, current_app, request
import io
import sys
import cv2
from pyzbar import pyzbar

from flaskr.data_store.db import get_db
from ..helpers.openlibrary_engine import OpenLibraryClient

bp = Blueprint('scanner', __name__, url_prefix="/scanner")

@bp.route('/output/<isbn>')
def output(isbn):  
    
    return redirect(url_for('home.book_details', id=isbn))

@bp.route('/scanner')
def scanner():
    return render_template('scanner/scanner.html')