/* OLD DB CREANUP */

DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS checkout_log;
DROP TABLE IF EXISTS login;
DROP TABLE IF EXISTS library;
DROP TABLE IF EXISTS library_book;
DROP TRIGGER IF EXISTS user_username_default_value;

/* TABLE CREATION */

CREATE TABLE author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    olid TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    isbn INTEGER NOT NULL,
    illustration_url TEXT NOT NULL,
    olid TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (author_id) REFERENCES author (id),
    UNIQUE(isbn)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    library_card_number INTEGER NOT NULL,
    is_admin BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (username) 
);

CREATE TABLE login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE(username)
);

CREATE TABLE checkout_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    checkout_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    checkout_duration INTEGER NOT NULL,
    checkin_date TIMESTAMP,
    renew_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (book_id) REFERENCES book (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSe,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE library_book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    library_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

/* TRIGER CREATION */

CREATE TRIGGER user_username_default_value
AFTER INSERT ON user
FOR EACH ROW
WHEN NEW.username IS NULL
BEGIN
    UPDATE user
    SET username = NEW.first_name || NEW.last_name;
END;